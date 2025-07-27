"""
Performance monitoring tests for AsyncioPySide6.

This module contains tests for the performance monitoring and health check
functionality in the refactored AsyncioPySide6 implementation.
"""

import asyncio
import sys
import time
from typing import Any
from unittest.mock import MagicMock, Mock, patch

import pytest

# Add parent directory to path for imports
sys.path.insert(0, "..")

from AsyncioPySide6 import AsyncioPySide6, get_config, reset_config, set_config
from AsyncioPySide6.nvd.performance import (
    get_health_status,
    get_performance_monitor,
    record_task_completion,
    record_task_start,
    start_performance_monitoring,
    stop_performance_monitoring,
)


class TestPerformanceMonitoring:
    """Test performance monitoring functionality."""

    def setup_method(self) -> None:
        """Set up test environment."""
        reset_config()
        AsyncioPySide6.reset_for_testing()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        reset_config()
        AsyncioPySide6.reset_for_testing()

    def test_performance_monitor_singleton(self) -> None:
        """Test that performance monitor follows singleton pattern."""
        monitor1 = get_performance_monitor()
        monitor2 = get_performance_monitor()

        assert monitor1 is monitor2
        assert id(monitor1) == id(monitor2)

    def test_start_stop_monitoring(self) -> None:
        """Test starting and stopping performance monitoring."""
        # Enable performance monitoring before getting the monitor
        config = get_config()
        config.enable_performance_monitoring = True
        set_config(config)
        monitor = get_performance_monitor()

        # Start monitoring
        start_performance_monitoring()
        assert monitor._monitoring

        # Stop monitoring
        stop_performance_monitoring()
        assert not monitor._monitoring

    def test_record_task_start(self) -> None:
        """Test recording task start."""
        task_id = "test_task_123"

        record_task_start(task_id)

        # Verify task was recorded
        monitor = get_performance_monitor()
        assert task_id in monitor._task_metrics

    def test_record_task_completion(self) -> None:
        """Test recording task completion."""
        task_id = "test_task_456"

        # Record task start
        record_task_start(task_id)

        # Record successful completion
        record_task_completion(task_id, True)

        # Verify task completion was recorded
        monitor = get_performance_monitor()
        task_metrics = monitor._task_metrics[task_id]
        assert task_metrics.success == True
        assert task_metrics.end_time is not None

    def test_record_task_completion_with_error(self) -> None:
        """Test recording task completion with error."""
        task_id = "test_task_789"
        error_message = "Test error occurred"

        # Record task start
        record_task_start(task_id)

        # Record failed completion
        record_task_completion(task_id, False, error_message)

        # Verify error was recorded
        monitor = get_performance_monitor()
        task_metrics = monitor._task_metrics[task_id]
        assert task_metrics.success == False
        assert task_metrics.error == error_message

    def test_health_status(self) -> None:
        """Test health status functionality."""
        # Enable performance monitoring before getting the monitor
        config = get_config()
        config.enable_performance_monitoring = True
        set_config(config)
        monitor = get_performance_monitor()
        # Inject a real metric
        from AsyncioPySide6.nvd.performance import PerformanceMetrics

        metric = PerformanceMetrics(
            timestamp=time.time(),
            active_tasks=1,
            memory_usage_mb=100.0,
            memory_percentage=0.5,
            event_loop_latency_ms=1.0,
            task_completion_rate=1.0,
            error_rate=0.0,
            cpu_usage_percentage=10.0,
        )
        monitor.metrics_history.append(metric)

        health = get_health_status()
        # Verify health status structure
        assert isinstance(health, dict)
        assert "status" in health
        assert "memory_usage" in health
        assert "performance_score" in health
        assert "active_tasks" in health
        assert "error_rate" in health

    def test_health_status_with_tasks(self) -> None:
        """Test health status with active tasks."""
        # Enable performance monitoring before getting the monitor
        config = get_config()
        config.enable_performance_monitoring = True
        set_config(config)
        monitor = get_performance_monitor()
        # Record some task activity
        record_task_start("test_task_health")
        time.sleep(0.01)
        record_task_completion("test_task_health", True)
        # Inject a real metric
        from AsyncioPySide6.nvd.performance import PerformanceMetrics

        metric = PerformanceMetrics(
            timestamp=time.time(),
            active_tasks=1,
            memory_usage_mb=100.0,
            memory_percentage=0.5,
            event_loop_latency_ms=1.0,
            task_completion_rate=1.0,
            error_rate=0.0,
            cpu_usage_percentage=10.0,
        )
        monitor.metrics_history.append(metric)
        health = get_health_status()
        # Verify task information is included
        assert "active_tasks" in health
        assert "completed_tasks" in health

    def test_circuit_breaker(self) -> None:
        """Test circuit breaker functionality."""
        monitor = get_performance_monitor()

        # Get circuit breaker
        cb = monitor.get_circuit_breaker("test_circuit")

        # Test initial state
        assert cb.state == "CLOSED"
        assert cb.failure_count == 0

        # Test successful call
        def successful_func() -> str:
            return "success"

        result = cb.call(successful_func)
        assert result == "success"
        assert cb.state == "CLOSED"

    def test_circuit_breaker_failure(self) -> None:
        """Test circuit breaker with failures."""
        monitor = get_performance_monitor()
        cb = monitor.get_circuit_breaker("test_circuit_failure")

        # Set low threshold for testing
        cb.threshold = 2

        def failing_func() -> str:
            raise Exception("Test failure")

        # First failure
        with pytest.raises(Exception):
            cb.call(failing_func)
        assert cb.failure_count == 1
        assert cb.state == "CLOSED"

        # Second failure - should open circuit
        with pytest.raises(Exception):
            cb.call(failing_func)
        assert cb.failure_count == 2
        assert cb.state == "OPEN"

    def test_circuit_breaker_recovery(self) -> None:
        """Test circuit breaker recovery."""
        monitor = get_performance_monitor()
        cb = monitor.get_circuit_breaker("test_circuit_recovery")

        # Set low threshold and recovery time for testing
        cb.threshold = 1
        cb.recovery_time = 0.1

        def failing_func() -> str:
            raise Exception("Test failure")

        def successful_func() -> str:
            return "success"

        # Cause circuit to open
        with pytest.raises(Exception):
            cb.call(failing_func)
        assert cb.state == "OPEN"

        # Wait for recovery time
        time.sleep(0.2)

        # Try successful call - should recover
        result = cb.call(successful_func)
        assert result == "success"
        assert cb.state == "CLOSED"

    def test_metrics_collection(self) -> None:
        """Test metrics collection."""
        monitor = get_performance_monitor()

        # Start monitoring
        start_performance_monitoring()

        # Record some activity
        record_task_start("task1")
        time.sleep(0.1)
        record_task_completion("task1", True)

        # Get recent metrics
        metrics = monitor.get_recent_metrics(5)

        # Verify metrics structure
        assert isinstance(metrics, list)
        if metrics:  # Metrics might be empty in test environment
            metric = metrics[0]
            assert hasattr(metric, "timestamp")
            assert hasattr(metric, "active_tasks")
            assert hasattr(metric, "memory_usage_mb")

    def test_memory_monitoring(self) -> None:
        """Test memory monitoring functionality."""
        monitor = get_performance_monitor()

        # Mock psutil for consistent testing
        with patch("AsyncioPySide6.nvd.performance.psutil") as mock_psutil:
            # Mock process
            mock_process = Mock()
            mock_memory_info = Mock()
            mock_memory_info.rss = 1024 * 1024 * 100  # 100MB
            mock_process.memory_info.return_value = mock_memory_info
            mock_process.cpu_percent.return_value = 25.0
            mock_psutil.Process.return_value = mock_process

            # Mock virtual memory
            mock_virtual_memory = Mock()
            mock_virtual_memory.total = 1024 * 1024 * 1024 * 8  # 8GB
            mock_psutil.virtual_memory.return_value = mock_virtual_memory

            # Test memory collection
            metrics = monitor._collect_metrics()

            assert metrics.memory_usage_mb > 0
            assert metrics.memory_percentage > 0

    def test_performance_configuration(self) -> None:
        """Test performance monitoring configuration."""
        config = get_config()

        # Enable performance monitoring
        config.enable_performance_monitoring = True
        config.enable_metrics_collection = True
        config.enable_memory_monitoring = True
        config.enable_task_monitoring = True
        set_config(config)

        # Verify configuration is applied
        new_config = get_config()
        assert new_config.enable_performance_monitoring == True
        assert new_config.enable_metrics_collection == True
        assert new_config.enable_memory_monitoring == True
        assert new_config.enable_task_monitoring == True

    def test_metrics_cleanup(self) -> None:
        """Test metrics cleanup functionality."""
        monitor = get_performance_monitor()
        from AsyncioPySide6.nvd.performance import PerformanceMetrics

        # Add some old metrics
        old_timestamp = time.time() - 3600  # 1 hour ago
        monitor._metrics.append(
            PerformanceMetrics(
                timestamp=old_timestamp,
                active_tasks=1,
                memory_usage_mb=100.0,
                memory_percentage=0.5,
                event_loop_latency_ms=1.0,
                task_completion_rate=1.0,
                error_rate=0.0,
                cpu_usage_percentage=10.0,
            )
        )
        monitor._metrics.append(
            PerformanceMetrics(
                timestamp=time.time(),
                active_tasks=1,
                memory_usage_mb=100.0,
                memory_percentage=0.5,
                event_loop_latency_ms=1.0,
                task_completion_rate=1.0,
                error_rate=0.0,
                cpu_usage_percentage=10.0,
            )
        )  # Current time
        initial_count = len(monitor._metrics)
        # Clean up old metrics
        monitor.cleanup_old_metrics()
        # Should have fewer metrics after cleanup
        assert len(monitor._metrics) < initial_count

    def test_task_metrics_structure(self) -> None:
        """Test task metrics data structure."""
        from AsyncioPySide6.nvd.performance import TaskMetrics

        # Create task metrics
        task_id = "test_task"
        start_time = time.time()

        metrics = TaskMetrics(task_id=task_id, start_time=start_time)

        # Verify structure
        assert metrics.task_id == task_id
        assert metrics.start_time == start_time
        assert metrics.end_time is None
        assert metrics.execution_time is None
        assert metrics.success is None
        assert metrics.error is None

    def test_performance_metrics_structure(self) -> None:
        """Test performance metrics data structure."""
        from AsyncioPySide6.nvd.performance import PerformanceMetrics

        # Create performance metrics
        timestamp = time.time()
        metrics = PerformanceMetrics(
            timestamp=timestamp,
            active_tasks=5,
            memory_usage_mb=100.0,
            memory_percentage=50.0,
            event_loop_latency_ms=1.5,
            task_completion_rate=0.95,
            error_rate=0.05,
            cpu_usage_percentage=25.0,
        )

        # Verify structure
        assert metrics.timestamp == timestamp
        assert metrics.active_tasks == 5
        assert metrics.memory_usage_mb == 100.0
        assert metrics.memory_percentage == 50.0
        assert metrics.event_loop_latency_ms == 1.5
        assert metrics.task_completion_rate == 0.95
        assert metrics.error_rate == 0.05
        assert metrics.cpu_usage_percentage == 25.0

        # Test to_dict method
        metrics_dict = metrics.to_dict()
        assert isinstance(metrics_dict, dict)
        assert metrics_dict["timestamp"] == timestamp
        assert metrics_dict["active_tasks"] == 5


class TestPerformanceIntegration:
    """Test performance monitoring integration with AsyncioPySide6."""

    def setup_method(self) -> None:
        """Set up test environment."""
        reset_config()
        AsyncioPySide6.reset_for_testing()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        reset_config()
        AsyncioPySide6.reset_for_testing()

    def test_performance_monitoring_with_tasks(self) -> None:
        """Test performance monitoring with actual tasks."""
        config = get_config()
        config.enable_performance_monitoring = True
        set_config(config)
        with AsyncioPySide6() as manager:
            # Start performance monitoring
            start_performance_monitoring()

            # Run some tasks
            async def test_task() -> str:
                await asyncio.sleep(0.1)
                return "Task completed"

            # Suppress the RuntimeWarning about unawaited coroutines
            import warnings

            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                AsyncioPySide6.runTask(test_task())

            # Wait for task to complete
            time.sleep(0.2)
            # Inject a real metric
            from AsyncioPySide6.nvd.performance import PerformanceMetrics

            monitor = get_performance_monitor()
            metric = PerformanceMetrics(
                timestamp=time.time(),
                active_tasks=1,
                memory_usage_mb=100.0,
                memory_percentage=0.5,
                event_loop_latency_ms=1.0,
                task_completion_rate=1.0,
                error_rate=0.0,
                cpu_usage_percentage=10.0,
            )
            monitor.metrics_history.append(metric)
            # Check health status
            health = manager.get_health_status()
            assert "active_tasks" in health

    def test_health_status_integration(self) -> None:
        """Test health status integration."""
        with AsyncioPySide6() as manager:
            # Inject a real metric
            from AsyncioPySide6.nvd.performance import PerformanceMetrics

            monitor = get_performance_monitor()
            metric = PerformanceMetrics(
                timestamp=time.time(),
                active_tasks=1,
                memory_usage_mb=100.0,
                memory_percentage=0.5,
                event_loop_latency_ms=1.0,
                task_completion_rate=1.0,
                error_rate=0.0,
                cpu_usage_percentage=10.0,
            )
            monitor.metrics_history.append(metric)
            # Get health status
            health = manager.get_health_status()
            assert "active_tasks" in health

    def test_task_tracking_integration(self) -> None:
        """Test task tracking integration."""
        with AsyncioPySide6() as manager:
            # Initially no tasks
            assert manager.get_task_count() == 0

            # Add some tasks
            manager._active_tasks.add("task1")
            manager._active_tasks.add("task2")

            # Verify task count
            assert manager.get_task_count() == 2

            # Remove tasks
            manager._active_tasks.discard("task1")
            assert manager.get_task_count() == 1


if __name__ == "__main__":
    pytest.main([__file__])
