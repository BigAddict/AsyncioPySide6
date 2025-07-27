"""
pyside6_asyncplus - Native asyncio support for PySide6 with advanced features.

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
    >>> from pyside6_asyncplus.app import run
    >>> with pyside6_asyncplus.app():
    ...     pyside6_asyncplus.app.runTask(my_coroutine())
"""

from typing import Any, Dict

# Import the main app interface
from .app import (
    App,
    app,
    run,
    run_with_timeout,
    run_with_retry,
    run_with_progress,
    invoke_in_gui_thread,
    is_initialized,
    get_health_status,
    get_task_count,
)

# Import core components
from .nvd.AsyncioPySide6 import AsyncioPySide6, use_asyncio
from .nvd.config import AsyncioPySide6Config, get_config, reset_config, set_config
from .nvd.exceptions import (
    AsyncioPySide6Error,
    ConfigurationError,
    EventLoopError,
    InitializationError,
    MemoryError,
    ResourceExhaustedError,
    ShutdownError,
    TaskExecutionError,
    TaskTimeoutError,
    ThreadSafetyError,
)
from .nvd.performance import (
    get_health_status as get_performance_health_status,
    get_performance_monitor,
    record_task_completion,
    record_task_start,
    start_performance_monitoring,
    stop_performance_monitoring,
)

# Version information
__version__ = "0.1.0"
__author__ = "David N. Maina(BigAddict)"
__description__ = "Native asyncio support for PySide6 with advanced features"

__all__ = [
    # Main app interface
    "App",
    "app",
    "run",
    "run_with_timeout",
    "run_with_retry",
    "run_with_progress",
    "invoke_in_gui_thread",
    "is_initialized",
    "get_health_status",
    "get_task_count",
    # Core library
    "AsyncioPySide6",
    "use_asyncio",
    "get_config",
    "set_config",
    "reset_config",
    "AsyncioPySide6Config",
    # Exceptions
    "AsyncioPySide6Error",
    "EventLoopError",
    "ThreadSafetyError",
    "InitializationError",
    "ShutdownError",
    "TaskTimeoutError",
    "ResourceExhaustedError",
    "ConfigurationError",
    "TaskExecutionError",
    "MemoryError",
    # Performance monitoring
    "get_performance_monitor",
    "start_performance_monitoring",
    "stop_performance_monitoring",
    "record_task_start",
    "record_task_completion",
    "get_performance_health_status",
    # Version information
    "__version__",
    "__author__",
    "__description__",
]


def get_version() -> str:
    """Get the library version.

    Returns:
        str: The current version of pyside6_asyncplus
    """
    return __version__


def get_async_backends() -> Dict[str, Any]:
    """
    Get information about available async backends.

    Returns:
        dict: Dictionary with information about available backends and their capabilities
    """
    backends = {}

    # Our enhanced implementation
    backends["pyside6_asyncplus"] = {
        "available": True,
        "name": "pyside6_asyncplus",
        "description": "Native asyncio support for PySide6 with advanced features",
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
            "backward_compatibility",
        ],
    }

    return backends


def recommend_async_approach() -> Dict[str, Any]:
    """
    Recommend the best async approach based on available backends and requirements.

    Returns:
        dict: Dictionary with recommendations for different use cases
    """
    backends = get_async_backends()

    recommendations = {
        "simple_usage": {"recommendation": "pyside6_asyncplus", "reason": "Simple async tasks with QtAsyncio integration"},
        "production_usage": {
            "recommendation": "pyside6_asyncplus",
            "reason": "Production applications need comprehensive error handling and monitoring",
        },
        "advanced_features": {
            "recommendation": "pyside6_asyncplus",
            "reason": "Advanced features like timeout, retry, and progress tracking",
        },
        "gui_applications": {"recommendation": "pyside6_asyncplus", "reason": "Seamless integration with Qt GUI applications"},
    }

    return recommendations


def is_qtasyncio_available() -> bool:
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


def get_qtasyncio_info() -> Dict[str, Any]:
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
        "features": ["basic_async", "qt_integration", "signal_handling", "debug_mode"] if qtasyncio_available else [],
    }

    return info
