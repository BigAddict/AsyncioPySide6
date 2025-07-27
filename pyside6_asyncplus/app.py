"""
Main application interface for pyside6_asyncplus.

This module provides the primary interface for using pyside6_asyncplus
with PySide6 applications.
"""

from typing import Any, Callable, Optional
import asyncio

from .nvd.AsyncioPySide6 import AsyncioPySide6


class App:
    """Main application class for pyside6_asyncplus."""
    
    def __init__(self):
        self._asyncio_app = AsyncioPySide6()
    
    def __enter__(self):
        """Enter the application context."""
        self._asyncio_app.__enter__()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the application context."""
        self._asyncio_app.__exit__(exc_type, exc_val, exc_tb)
    
    @staticmethod
    def runTask(coro):
        """Run a basic async task."""
        return AsyncioPySide6.runTask(coro)
    
    @staticmethod
    def runTaskWithTimeout(coro, timeout: float):
        """Run task with timeout."""
        return AsyncioPySide6.runTaskWithTimeout(coro, timeout)
    
    @staticmethod
    def runTaskWithRetry(coro_func: Callable, max_retries: int = 3, retry_delay: float = 1.0):
        """Run task with retry logic."""
        return AsyncioPySide6.runTaskWithRetry(coro_func, max_retries, retry_delay)
    
    @staticmethod
    def runTaskWithProgress(coro, progress_callback: Optional[Callable] = None):
        """Run task with thread-safe progress tracking."""
        return AsyncioPySide6.runTaskWithProgress(coro, progress_callback)
    
    @staticmethod
    def invokeInGuiThread(gui_object, callable):
        """Safe GUI thread invocation."""
        return AsyncioPySide6.invokeInGuiThread(gui_object, callable)
    
    @staticmethod
    def is_initialized():
        """Check if initialized."""
        return AsyncioPySide6.is_initialized()
    
    @staticmethod
    def get_health_status():
        """Get system health status."""
        return AsyncioPySide6.get_health_status()
    
    @staticmethod
    def get_task_count():
        """Get active task count."""
        return AsyncioPySide6.get_task_count()


# Create a global instance for convenience
app = App()


def run(coro):
    """Run a basic async task using the global app instance."""
    return app.runTask(coro)


def run_with_timeout(coro, timeout: float):
    """Run task with timeout using the global app instance."""
    return app.runTaskWithTimeout(coro, timeout)


def run_with_retry(coro_func: Callable, max_retries: int = 3, retry_delay: float = 1.0):
    """Run task with retry logic using the global app instance."""
    return app.runTaskWithRetry(coro_func, max_retries, retry_delay)


def run_with_progress(coro, progress_callback: Optional[Callable] = None):
    """Run task with thread-safe progress tracking using the global app instance."""
    return app.runTaskWithProgress(coro, progress_callback)


def invoke_in_gui_thread(gui_object, callable):
    """Safe GUI thread invocation using the global app instance."""
    return app.invokeInGuiThread(gui_object, callable)


def is_initialized():
    """Check if initialized using the global app instance."""
    return app.is_initialized()


def get_health_status():
    """Get system health status using the global app instance."""
    return app.get_health_status()


def get_task_count():
    """Get active task count using the global app instance."""
    return app.get_task_count()


# Export the main classes and functions
__all__ = [
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
] 