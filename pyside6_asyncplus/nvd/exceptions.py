"""
Exception hierarchy for AsyncioPySide6.

This module defines all custom exceptions used by the library.
"""


class AsyncioPySide6Error(Exception):
    """Base exception for AsyncioPySide6 library"""

    pass


class EventLoopError(AsyncioPySide6Error):
    """Raised when event loop operations fail"""

    pass


class ThreadSafetyError(AsyncioPySide6Error):
    """Raised when thread safety is violated"""

    pass


class InitializationError(AsyncioPySide6Error):
    """Raised when initialization fails"""

    pass


class ShutdownError(AsyncioPySide6Error):
    """Raised when shutdown fails"""

    pass


class TaskTimeoutError(AsyncioPySide6Error):
    """Raised when a task exceeds its timeout"""

    pass


class ResourceExhaustedError(AsyncioPySide6Error):
    """Raised when resource limits are exceeded"""

    pass


class ConfigurationError(AsyncioPySide6Error):
    """Raised when configuration is invalid"""

    pass


class TaskExecutionError(AsyncioPySide6Error):
    """Raised when task execution fails"""

    pass


class MemoryError(AsyncioPySide6Error):
    """Raised when memory limits are exceeded"""

    pass
