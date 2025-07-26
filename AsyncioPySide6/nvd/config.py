"""
Configuration module for AsyncioPySide6.

This module provides a centralized configuration system for the AsyncioPySide6 library,
allowing users to customize various aspects of the library's behavior.
"""

import os
from dataclasses import dataclass, field
from typing import Optional
import logging


@dataclass
class AsyncioPySide6Config:
    """
    Configuration class for AsyncioPySide6.
    
    This class holds all configurable parameters for the library.
    Values can be set programmatically or through environment variables.
    """
    
    # Event loop configuration
    event_loop_interval: float = 0.01  # Increased from 0.001 for better stability
    idle_sleep_time: float = 0.01      # Increased from 0.001 for better stability
    use_dedicated_thread: bool = True   # Changed to True for better thread safety
    
    # Timeout configuration
    initialization_timeout: float = 5.0
    shutdown_timeout: float = 10.0
    task_timeout: float = 30.0
    
    # Retry configuration
    max_retries: int = 3
    retry_delay: float = 0.1
    
    # Logging configuration
    enable_logging: bool = True
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Performance configuration
    max_concurrent_tasks: int = 100
    task_queue_size: int = 1000
    
    # Debug configuration
    enable_debug_mode: bool = False
    enable_performance_monitoring: bool = False
    
    # Performance monitoring configuration
    enable_metrics_collection: bool = True
    metrics_interval: float = 5.0  # Metrics collection interval in seconds
    enable_memory_monitoring: bool = True
    memory_warning_threshold: float = 0.8  # 80% memory usage warning
    enable_task_monitoring: bool = True
    max_task_execution_time: float = 300.0  # 5 minutes max task time
    
    # Circuit breaker configuration
    enable_circuit_breaker: bool = False
    circuit_breaker_threshold: int = 5
    circuit_breaker_timeout: float = 60.0
    circuit_breaker_recovery_time: float = 300.0
    
    def __post_init__(self):
        """Validate configuration after initialization"""
        self._validate_config()
        self._setup_logging()
    
    def _validate_config(self):
        """Validate configuration parameters"""
        if self.event_loop_interval <= 0:
            raise ValueError("event_loop_interval must be positive")
        
        if self.idle_sleep_time <= 0:
            raise ValueError("idle_sleep_time must be positive")
        
        if self.initialization_timeout <= 0:
            raise ValueError("initialization_timeout must be positive")
        
        if self.shutdown_timeout <= 0:
            raise ValueError("shutdown_timeout must be positive")
        
        if self.task_timeout <= 0:
            raise ValueError("task_timeout must be positive")
        
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        
        if self.retry_delay < 0:
            raise ValueError("retry_delay must be non-negative")
        
        if self.max_concurrent_tasks <= 0:
            raise ValueError("max_concurrent_tasks must be positive")
        
        if self.task_queue_size <= 0:
            raise ValueError("task_queue_size must be positive")
    
    def _setup_logging(self):
        """Setup logging configuration"""
        if self.enable_logging:
            logging.basicConfig(
                level=getattr(logging, self.log_level.upper()),
                format=self.log_format
            )
    
    @classmethod
    def from_environment(cls) -> 'AsyncioPySide6Config':
        """
        Create configuration from environment variables.
        
        Environment variables:
        - ASYNCIOPYSIDE6_EVENT_LOOP_INTERVAL: Event loop interval in seconds
        - ASYNCIOPYSIDE6_IDLE_SLEEP_TIME: Idle sleep time in seconds
        - ASYNCIOPYSIDE6_USE_DEDICATED_THREAD: Use dedicated thread (true/false)
        - ASYNCIOPYSIDE6_INIT_TIMEOUT: Initialization timeout in seconds
        - ASYNCIOPYSIDE6_SHUTDOWN_TIMEOUT: Shutdown timeout in seconds
        - ASYNCIOPYSIDE6_TASK_TIMEOUT: Task timeout in seconds
        - ASYNCIOPYSIDE6_MAX_RETRIES: Maximum retry attempts
        - ASYNCIOPYSIDE6_RETRY_DELAY: Retry delay in seconds
        - ASYNCIOPYSIDE6_ENABLE_LOGGING: Enable logging (true/false)
        - ASYNCIOPYSIDE6_LOG_LEVEL: Log level (DEBUG, INFO, WARNING, ERROR)
        - ASYNCIOPYSIDE6_MAX_CONCURRENT_TASKS: Maximum concurrent tasks
        - ASYNCIOPYSIDE6_TASK_QUEUE_SIZE: Task queue size
        - ASYNCIOPYSIDE6_ENABLE_DEBUG_MODE: Enable debug mode (true/false)
        - ASYNCIOPYSIDE6_ENABLE_PERFORMANCE_MONITORING: Enable performance monitoring (true/false)
        """
        config = cls()
        
        # Event loop configuration
        if os.getenv('ASYNCIOPYSIDE6_EVENT_LOOP_INTERVAL'):
            config.event_loop_interval = float(os.getenv('ASYNCIOPYSIDE6_EVENT_LOOP_INTERVAL'))
        
        if os.getenv('ASYNCIOPYSIDE6_IDLE_SLEEP_TIME'):
            config.idle_sleep_time = float(os.getenv('ASYNCIOPYSIDE6_IDLE_SLEEP_TIME'))
        
        if os.getenv('ASYNCIOPYSIDE6_USE_DEDICATED_THREAD'):
            config.use_dedicated_thread = os.getenv('ASYNCIOPYSIDE6_USE_DEDICATED_THREAD').lower() == 'true'
        
        # Timeout configuration
        if os.getenv('ASYNCIOPYSIDE6_INIT_TIMEOUT'):
            config.initialization_timeout = float(os.getenv('ASYNCIOPYSIDE6_INIT_TIMEOUT'))
        
        if os.getenv('ASYNCIOPYSIDE6_SHUTDOWN_TIMEOUT'):
            config.shutdown_timeout = float(os.getenv('ASYNCIOPYSIDE6_SHUTDOWN_TIMEOUT'))
        
        if os.getenv('ASYNCIOPYSIDE6_TASK_TIMEOUT'):
            config.task_timeout = float(os.getenv('ASYNCIOPYSIDE6_TASK_TIMEOUT'))
        
        # Retry configuration
        if os.getenv('ASYNCIOPYSIDE6_MAX_RETRIES'):
            config.max_retries = int(os.getenv('ASYNCIOPYSIDE6_MAX_RETRIES'))
        
        if os.getenv('ASYNCIOPYSIDE6_RETRY_DELAY'):
            config.retry_delay = float(os.getenv('ASYNCIOPYSIDE6_RETRY_DELAY'))
        
        # Logging configuration
        if os.getenv('ASYNCIOPYSIDE6_ENABLE_LOGGING'):
            config.enable_logging = os.getenv('ASYNCIOPYSIDE6_ENABLE_LOGGING').lower() == 'true'
        
        if os.getenv('ASYNCIOPYSIDE6_LOG_LEVEL'):
            config.log_level = os.getenv('ASYNCIOPYSIDE6_LOG_LEVEL').upper()
        
        # Performance configuration
        if os.getenv('ASYNCIOPYSIDE6_MAX_CONCURRENT_TASKS'):
            config.max_concurrent_tasks = int(os.getenv('ASYNCIOPYSIDE6_MAX_CONCURRENT_TASKS'))
        
        if os.getenv('ASYNCIOPYSIDE6_TASK_QUEUE_SIZE'):
            config.task_queue_size = int(os.getenv('ASYNCIOPYSIDE6_TASK_QUEUE_SIZE'))
        
        # Debug configuration
        if os.getenv('ASYNCIOPYSIDE6_ENABLE_DEBUG_MODE'):
            config.enable_debug_mode = os.getenv('ASYNCIOPYSIDE6_ENABLE_DEBUG_MODE').lower() == 'true'
        
        if os.getenv('ASYNCIOPYSIDE6_ENABLE_PERFORMANCE_MONITORING'):
            config.enable_performance_monitoring = os.getenv('ASYNCIOPYSIDE6_ENABLE_PERFORMANCE_MONITORING').lower() == 'true'
        
        return config
    
    def to_dict(self) -> dict:
        """Convert configuration to dictionary"""
        return {
            'event_loop_interval': self.event_loop_interval,
            'idle_sleep_time': self.idle_sleep_time,
            'use_dedicated_thread': self.use_dedicated_thread,
            'initialization_timeout': self.initialization_timeout,
            'shutdown_timeout': self.shutdown_timeout,
            'task_timeout': self.task_timeout,
            'max_retries': self.max_retries,
            'retry_delay': self.retry_delay,
            'enable_logging': self.enable_logging,
            'log_level': self.log_level,
            'log_format': self.log_format,
            'max_concurrent_tasks': self.max_concurrent_tasks,
            'task_queue_size': self.task_queue_size,
            'enable_debug_mode': self.enable_debug_mode,
            'enable_performance_monitoring': self.enable_performance_monitoring,
        }
    
    def __str__(self) -> str:
        """String representation of configuration"""
        return f"AsyncioPySide6Config({', '.join(f'{k}={v}' for k, v in self.to_dict().items())})"


# Global configuration instance
_config: Optional[AsyncioPySide6Config] = None


def get_config() -> AsyncioPySide6Config:
    """Get the global configuration instance"""
    global _config
    if _config is None:
        _config = AsyncioPySide6Config.from_environment()
    return _config


def set_config(config: AsyncioPySide6Config) -> None:
    """Set the global configuration instance"""
    global _config
    _config = config


def reset_config() -> None:
    """Reset the global configuration to default"""
    global _config
    _config = None 