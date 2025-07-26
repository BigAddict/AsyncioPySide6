"""
Performance monitoring module for AsyncioPySide6.

This module provides comprehensive performance monitoring capabilities including
memory usage tracking, task execution metrics, and health checks.
"""

import asyncio
import time
import threading
import psutil
import logging
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from collections import defaultdict, deque
from .config import get_config, AsyncioPySide6Config
from .exceptions import ResourceExhaustedError

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetrics:
    """Performance metrics data class"""
    timestamp: float
    active_tasks: int
    memory_usage_mb: float
    memory_percentage: float
    event_loop_latency_ms: float
    task_completion_rate: float
    error_rate: float
    cpu_usage_percentage: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary"""
        return {
            'timestamp': self.timestamp,
            'active_tasks': self.active_tasks,
            'memory_usage_mb': self.memory_usage_mb,
            'memory_percentage': self.memory_percentage,
            'event_loop_latency_ms': self.event_loop_latency_ms,
            'task_completion_rate': self.task_completion_rate,
            'error_rate': self.error_rate,
            'cpu_usage_percentage': self.cpu_usage_percentage
        }


@dataclass
class TaskMetrics:
    """Task execution metrics"""
    task_id: str
    start_time: float
    end_time: Optional[float] = None
    execution_time: Optional[float] = None
    success: Optional[bool] = None
    error: Optional[str] = None
    memory_usage: Optional[float] = None


class CircuitBreaker:
    """Circuit breaker pattern for fault tolerance"""
    
    def __init__(self, threshold: int = 5, timeout: float = 60.0, recovery_time: float = 300.0):
        self.threshold = threshold
        self.timeout = timeout
        self.recovery_time = recovery_time
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self._lock = threading.Lock()
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection"""
        with self._lock:
            if self.state == "OPEN":
                if time.time() - self.last_failure_time > self.recovery_time:
                    self.state = "HALF_OPEN"
                else:
                    raise ResourceExhaustedError("Circuit breaker is OPEN")
            
            try:
                result = func(*args, **kwargs)
                if self.state == "HALF_OPEN":
                    self.state = "CLOSED"
                    self.failure_count = 0
                return result
            except Exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()
                
                if self.failure_count >= self.threshold:
                    self.state = "OPEN"
                
                raise e


class PerformanceMonitor:
    """Performance monitoring and metrics collection"""
    
    def __init__(self):
        self.config = get_config()
        self.metrics_history: deque = deque(maxlen=1000)
        self.task_metrics: Dict[str, TaskMetrics] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self._monitoring_task: Optional[asyncio.Task] = None
        self._stop_monitoring = threading.Event()
        self._lock = threading.Lock()
        
        # Performance counters
        self._task_count = 0
        self._error_count = 0
        self._start_time = time.time()
        self._last_metrics_time = time.time()
    
    def start_monitoring(self) -> None:
        """Start performance monitoring"""
        if not self.config.enable_performance_monitoring:
            return
        
        if self._monitoring_task is None:
            self._stop_monitoring.clear()
            # Use a different approach to avoid coroutine warnings
            self._monitoring_task = asyncio.create_task(self._monitor_loop())
            logger.info("Performance monitoring started")
    
    def stop_monitoring(self) -> None:
        """Stop performance monitoring"""
        if self._monitoring_task:
            self._stop_monitoring.set()
            try:
                self._monitoring_task.cancel()
            except Exception:
                pass
            self._monitoring_task = None
            logger.info("Performance monitoring stopped")
    
    async def _monitor_loop(self) -> None:
        """Main monitoring loop"""
        try:
            while not self._stop_monitoring.is_set():
                try:
                    metrics = self._collect_metrics()
                    self.metrics_history.append(metrics)
                    
                    # Check for memory warnings
                    if (self.config.enable_memory_monitoring and 
                        metrics.memory_percentage > self.config.memory_warning_threshold):
                        logger.warning(f"High memory usage: {metrics.memory_percentage:.1f}%")
                    
                    # Check for performance issues
                    if metrics.event_loop_latency_ms > 100:  # 100ms threshold
                        logger.warning(f"High event loop latency: {metrics.event_loop_latency_ms:.2f}ms")
                    
                    await asyncio.sleep(self.config.metrics_interval)
                    
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.error(f"Error in monitoring loop: {e}")
                    await asyncio.sleep(1.0)
        except Exception as e:
            logger.error(f"Fatal error in monitoring loop: {e}")
    
    def _collect_metrics(self) -> PerformanceMetrics:
        """Collect current performance metrics"""
        process = psutil.Process()
        memory_info = process.memory_info()
        
        # Calculate memory usage
        memory_usage_mb = memory_info.rss / 1024 / 1024
        memory_percentage = memory_info.rss / psutil.virtual_memory().total
        
        # Calculate CPU usage
        cpu_percentage = process.cpu_percent()
        
        # Calculate task completion rate
        current_time = time.time()
        time_window = current_time - self._last_metrics_time
        task_completion_rate = self._task_count / max(time_window, 1.0)
        error_rate = self._error_count / max(time_window, 1.0)
        
        # Reset counters
        self._task_count = 0
        self._error_count = 0
        self._last_metrics_time = current_time
        
        # Calculate event loop latency (simplified)
        event_loop_latency = 0.0  # This would need actual measurement
        
        return PerformanceMetrics(
            timestamp=current_time,
            active_tasks=len(self.task_metrics),
            memory_usage_mb=memory_usage_mb,
            memory_percentage=memory_percentage,
            event_loop_latency_ms=event_loop_latency,
            task_completion_rate=task_completion_rate,
            error_rate=error_rate,
            cpu_usage_percentage=cpu_percentage
        )
    
    def record_task_start(self, task_id: str) -> None:
        """Record task start"""
        with self._lock:
            self.task_metrics[task_id] = TaskMetrics(
                task_id=task_id,
                start_time=time.time()
            )
            self._task_count += 1
    
    def record_task_completion(self, task_id: str, success: bool, error: Optional[str] = None) -> None:
        """Record task completion"""
        with self._lock:
            if task_id in self.task_metrics:
                task_metric = self.task_metrics[task_id]
                task_metric.end_time = time.time()
                task_metric.execution_time = task_metric.end_time - task_metric.start_time
                task_metric.success = success
                task_metric.error = error
                
                if not success:
                    self._error_count += 1
    
    def get_circuit_breaker(self, name: str) -> CircuitBreaker:
        """Get or create a circuit breaker"""
        if name not in self.circuit_breakers:
            self.circuit_breakers[name] = CircuitBreaker(
                threshold=self.config.circuit_breaker_threshold,
                timeout=self.config.circuit_breaker_timeout,
                recovery_time=self.config.circuit_breaker_recovery_time
            )
        return self.circuit_breakers[name]
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get current health status"""
        if not self.metrics_history:
            return {"status": "unknown", "message": "No metrics available"}
        
        latest_metrics = self.metrics_history[-1]
        
        # Determine health status
        if latest_metrics.memory_percentage > 0.9:
            status = "critical"
            message = "Memory usage critical"
        elif latest_metrics.memory_percentage > 0.8:
            status = "warning"
            message = "Memory usage high"
        elif latest_metrics.error_rate > 0.1:
            status = "warning"
            message = "High error rate"
        else:
            status = "healthy"
            message = "All systems operational"
        
        return {
            "status": status,
            "message": message,
            "metrics": latest_metrics.to_dict(),
            "uptime": time.time() - self._start_time
        }
    
    def get_recent_metrics(self, count: int = 10) -> List[PerformanceMetrics]:
        """Get recent performance metrics"""
        return list(self.metrics_history)[-count:]
    
    def cleanup_old_metrics(self) -> None:
        """Clean up old task metrics"""
        current_time = time.time()
        with self._lock:
            # Remove task metrics older than 1 hour
            cutoff_time = current_time - 3600
            self.task_metrics = {
                task_id: metric for task_id, metric in self.task_metrics.items()
                if metric.end_time is None or metric.end_time > cutoff_time
            }


# Global performance monitor instance
_performance_monitor: Optional[PerformanceMonitor] = None


def get_performance_monitor() -> PerformanceMonitor:
    """Get the global performance monitor instance"""
    global _performance_monitor
    if _performance_monitor is None:
        _performance_monitor = PerformanceMonitor()
    return _performance_monitor


def start_performance_monitoring() -> None:
    """Start performance monitoring"""
    monitor = get_performance_monitor()
    monitor.start_monitoring()


def stop_performance_monitoring() -> None:
    """Stop performance monitoring"""
    global _performance_monitor
    if _performance_monitor:
        _performance_monitor.stop_monitoring()


def record_task_start(task_id: str) -> None:
    """Record task start"""
    monitor = get_performance_monitor()
    monitor.record_task_start(task_id)


def record_task_completion(task_id: str, success: bool, error: Optional[str] = None) -> None:
    """Record task completion"""
    monitor = get_performance_monitor()
    monitor.record_task_completion(task_id, success, error)


def get_health_status() -> Dict[str, Any]:
    """Get current health status"""
    monitor = get_performance_monitor()
    return monitor.get_health_status() 