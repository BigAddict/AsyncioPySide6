"""
AsyncioPySide6 - Enhanced QtAsyncio Integration.

This package provides an enhanced wrapper around PySide6's QtAsyncio that adds
advanced features like timeout handling, retry logic, performance monitoring,
and comprehensive error handling while maintaining full compatibility with QtAsyncio.

The package extends QtAsyncio with:
- Advanced task management (timeout, retry, progress)
- Performance monitoring and health checks
- Thread-safe GUI operations
- Comprehensive error handling
- Configuration system
- Backward compatibility with existing APIs

Example:
    >>> from AsyncioPySide6 import AsyncioPySide6
    >>> with AsyncioPySide6():
    ...     AsyncioPySide6.runTask(my_coroutine())
"""

from .nvd.AsyncioPySide6 import AsyncioPySide6, use_asyncio
from .nvd.config import get_config, set_config, reset_config, AsyncioPySide6Config
from .nvd.exceptions import (
    AsyncioPySide6Error,
    EventLoopError,
    ThreadSafetyError,
    InitializationError,
    ShutdownError,
    TaskTimeoutError,
    ResourceExhaustedError,
    ConfigurationError,
    TaskExecutionError,
    MemoryError
)
from .nvd.performance import (
    get_performance_monitor,
    start_performance_monitoring,
    stop_performance_monitoring,
    record_task_start,
    record_task_completion,
    get_health_status
)

# Version information
__version__ = "2.0.0"
__author__ = "AsyncioPySide6 Team"
__description__ = "Enhanced QtAsyncio integration with advanced async features"

__all__ = [
    # Core library
    'AsyncioPySide6',
    'use_asyncio',
    'get_config',
    'set_config', 
    'reset_config',
    'AsyncioPySide6Config',
    
    # Exceptions
    'AsyncioPySide6Error',
    'EventLoopError',
    'ThreadSafetyError',
    'InitializationError',
    'ShutdownError',
    'TaskTimeoutError',
    'ResourceExhaustedError',
    'ConfigurationError',
    'TaskExecutionError',
    'MemoryError',
    
    # Performance monitoring
    'get_performance_monitor',
    'start_performance_monitoring',
    'stop_performance_monitoring',
    'record_task_start',
    'record_task_completion',
    'get_health_status',
    
    # Version information
    '__version__',
    '__author__',
    '__description__'
]


def get_version():
    """Get the library version.
    
    Returns:
        str: The current version of AsyncioPySide6
    """
    return __version__


def get_async_backends():
    """
    Get information about available async backends.
    
    Returns:
        dict: Dictionary with information about available backends and their capabilities
    """
    backends = {}
    
    # Our enhanced implementation
    backends["asyncio_pyside6"] = {
        "available": True,
        "name": "AsyncioPySide6",
        "description": "Enhanced QtAsyncio integration with advanced features",
        "features": [
            "qtasyncio_integration",
            "advanced_task_management",
            "timeout_handling",
            "retry_logic",
            "progress_tracking",
            "performance_monitoring",
            "health_checks",
            "thread_safety",
            "gui_thread_safety",
            "comprehensive_error_handling",
            "configuration_system",
            "backward_compatibility"
        ]
    }
    
    return backends


def recommend_async_approach():
    """
    Recommend the best async approach based on available backends and requirements.
    
    Returns:
        dict: Dictionary with recommendations for different use cases
    """
    backends = get_async_backends()
    
    recommendations = {
        "simple_usage": {
            "recommendation": "asyncio_pyside6",
            "reason": "Simple async tasks with QtAsyncio integration"
        },
        "production_usage": {
            "recommendation": "asyncio_pyside6",
            "reason": "Production applications need comprehensive error handling and monitoring"
        },
        "advanced_features": {
            "recommendation": "asyncio_pyside6",
            "reason": "Advanced features like timeout, retry, and progress tracking"
        },
        "gui_applications": {
            "recommendation": "asyncio_pyside6",
            "reason": "Seamless integration with Qt GUI applications"
        }
    }
    
    return recommendations


def is_qtasyncio_available():
    """
    Check if QtAsyncio is available in the current PySide6 installation.
    
    Returns:
        bool: True if QtAsyncio is available, False otherwise
    """
    try:
        import PySide6.QtAsyncio as QtAsyncio
        return True
    except ImportError:
        return False


def get_qtasyncio_info():
    """
    Get information about QtAsyncio availability and features.
    
    Returns:
        dict: Dictionary with QtAsyncio information
    """
    qtasyncio_available = is_qtasyncio_available()
    
    info = {
        "available": qtasyncio_available,
        "name": "PySide6 QtAsyncio",
        "description": "Built-in async support for PySide6",
        "features": [
            "basic_async",
            "qt_integration",
            "signal_handling",
            "debug_mode"
        ] if qtasyncio_available else []
    }
    
    return info