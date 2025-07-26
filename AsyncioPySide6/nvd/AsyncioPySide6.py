import asyncio
import logging
import time
import threading
import warnings
import uuid
from typing import Optional, Callable, Coroutine, Any, Union

from PySide6.QtCore import QThread, QObject, QTimer
from .config import get_config
from .performance import record_task_start, record_task_completion, get_health_status
from .exceptions import (
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

def suppress_coroutine_warnings():
    """Suppress RuntimeWarnings for coroutines that are intentionally not awaited"""
    warnings.filterwarnings("ignore", message="coroutine.*was never awaited", category=RuntimeWarning)

class AsyncioByThread(QThread):
    def __init__(self):
        super().__init__()
        self.isShuttingDown = False
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self._initialized = False
        self._error = None
        self._loop_lock = threading.Lock()
        self._shutdown_event = threading.Event()

    def run(self):
        try:
            with self._loop_lock:
                self.loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.loop)
                self._initialized = True
            
            # Run the event loop until shutdown is requested
            while not self.isShuttingDown and not self._shutdown_event.is_set():
                try:
                    # Run the event loop for a short time
                    self.loop.run_until_complete(self._event_loop())
                except asyncio.CancelledError:
                    # This is expected during shutdown
                    break
                except Exception as e:
                    if not self.isShuttingDown:
                        logging.error(f"Error in event loop: {e}")
                        raise EventLoopError(f"Event loop error: {e}")
                    break
        except Exception as e:
            self._error = e
            logging.error(f"AsyncioByThread failed to initialize: {e}")
            raise EventLoopError(f"Failed to initialize event loop in thread: {e}")
        finally:
            self._cleanup_loop()

    async def _event_loop(self):
        config = get_config()
        try:
            await asyncio.sleep(config.idle_sleep_time)
        except asyncio.CancelledError:
            # Re-raise CancelledError to properly handle shutdown
            raise
        except Exception as e:
            logging.error(f"Error in event loop: {e}")
            if not self.isShuttingDown:
                raise EventLoopError(f"Event loop error: {e}")

    def _cleanup_loop(self):
        """Safely cleanup the event loop"""
        try:
            if self.loop and not self.loop.is_closed():
                # Cancel all pending tasks
                pending_tasks = asyncio.all_tasks(self.loop)
                for task in pending_tasks:
                    if not task.done():
                        task.cancel()
                
                # Run cleanup if there are pending tasks
                if pending_tasks:
                    try:
                        # Use gather with return_exceptions=True to handle cancelled tasks
                        self.loop.run_until_complete(
                            asyncio.gather(*pending_tasks, return_exceptions=True)
                        )
                    except Exception as e:
                        logging.warning(f"Error during task cleanup: {e}")
                
                # Close the loop
                self.loop.close()
        except Exception as e:
            logging.warning(f"Error during event loop cleanup: {e}")

    def run_event_loop(self):
        try:
            self.start()
            # Wait until the asyncio event loop is created with timeout
            config = get_config()
            timeout = config.initialization_timeout
            start_time = time.time()
            while self.loop is None and not self._error:
                if time.time() - start_time > timeout:
                    raise EventLoopError("Timeout waiting for event loop initialization")
                time.sleep(0.01)
            
            if self._error:
                raise self._error
                
        except Exception as e:
            logging.error(f"Failed to start event loop: {e}")
            raise EventLoopError(f"Failed to start event loop: {e}")

    def shutdown(self, timeout: float = None) -> bool:
        """Gracefully shutdown the thread-based event loop"""
        try:
            config = get_config()
            if timeout is None:
                timeout = config.shutdown_timeout
                
            self.isShuttingDown = True
            self._shutdown_event.set()
            
            # Signal shutdown to the event loop
            if self.loop and not self.loop.is_closed():
                try:
                    # Cancel all pending tasks
                    pending_tasks = asyncio.all_tasks(self.loop)
                    for task in pending_tasks:
                        if not task.done():
                            task.cancel()
                    
                    # Run cleanup if there are pending tasks
                    if pending_tasks:
                        try:
                            # Use gather with return_exceptions=True to handle cancelled tasks
                            self.loop.run_until_complete(
                                asyncio.gather(*pending_tasks, return_exceptions=True)
                            )
                        except Exception as e:
                            logging.warning(f"Error during task cleanup: {e}")
                except Exception as e:
                    logging.warning(f"Error during event loop cleanup: {e}")
            
            # Wait for thread to finish
            if not self.wait(int(timeout * 1000)):
                logging.warning(f"Thread shutdown timeout after {timeout} seconds")
                return False
                
            return True
        except Exception as e:
            logging.error(f"Error during thread shutdown: {e}")
            return False


class AsyncioByTimer(QTimer):
    def __init__(self):
        super().__init__()
       
        try:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
        except Exception as e:
            logging.error(f"Failed to create event loop: {e}")
            raise EventLoopError(f"Failed to create event loop: {e}")

        self.isShuttingDown = False
        self.timeout.connect(self._timer_timeout)
        config = get_config()
        self.setInterval(int(config.event_loop_interval * 1000))

    def _timer_timeout(self):
        try:
            if not self.isShuttingDown and self.loop and not self.loop.is_closed():
                # Run the event loop for a short time
                self.loop.run_until_complete(self._event_loop())
        except asyncio.CancelledError:
            # This is expected during shutdown
            pass
        except Exception as e:
            logging.error(f"Timer event loop error: {e}")
            if not self.isShuttingDown:
                raise EventLoopError(f"Timer event loop error: {e}")

    async def _event_loop(self):
        try:
            config = get_config()
            await asyncio.sleep(config.idle_sleep_time)
        except asyncio.CancelledError:
            # Re-raise CancelledError to properly handle shutdown
            raise
        except Exception as e:
            logging.error(f"Error in timer event loop: {e}")
            if not self.isShuttingDown:
                raise EventLoopError(f"Timer event loop error: {e}")

    def run_event_loop(self):
        try:
            self.start()
        except Exception as e:
            logging.error(f"Failed to start timer event loop: {e}")
            raise EventLoopError(f"Failed to start timer event loop: {e}")

    def shutdown(self, timeout: float = None) -> bool:
        """Gracefully shutdown the timer-based event loop"""
        try:
            config = get_config()
            if timeout is None:
                timeout = config.shutdown_timeout
                
            self.isShuttingDown = True
            self.stop()
            
            # Cancel all pending tasks
            if self.loop and not self.loop.is_closed():
                try:
                    pending_tasks = asyncio.all_tasks(self.loop)
                    for task in pending_tasks:
                        if not task.done():
                            task.cancel()
                    
                    # Run cleanup if there are pending tasks
                    if pending_tasks:
                        try:
                            # Use gather with return_exceptions=True to handle cancelled tasks
                            self.loop.run_until_complete(
                                asyncio.gather(*pending_tasks, return_exceptions=True)
                            )
                        except Exception as e:
                            logging.warning(f"Error during task cleanup: {e}")
                    
                    # Close the loop
                    self.loop.close()
                except Exception as e:
                    logging.warning(f"Error during timer event loop cleanup: {e}")
            
            return True
        except Exception as e:
            logging.error(f"Error during timer shutdown: {e}")
            return False


class AsyncioPySide6:
    """
    A utility class to simplify integration of asynchronous programming with Qt PySide6 projects.

    This class provides a thread-safe singleton pattern and manages the integration
    between asyncio event loops and Qt's event system.

    Usage:
    ```
    with AsyncioPySide6():
        # Your Qt PySide6 application code here
    ```

    Alternatively, you can use `AsyncioPySide6.init()` and `AsyncioPySide6.dispose()` 
    if the "with" statement is not preferred.
    """
    _instance: Optional['AsyncioPySide6'] = None
    _lock = threading.Lock()
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Prevent multiple initialization
        if self._initialized:
            return
            
        self._asyncioByThread: Optional[AsyncioByThread] = None
        self._asyncioByTimer: Optional[AsyncioByTimer] = None
        config = get_config()
        self._use_dedicated_thread: bool = config.use_dedicated_thread
        self._shutdown_called = False
        self._initialized = True
    
    def _reset_state(self):
        """Reset the internal state for testing purposes"""
        # Properly shutdown existing instances
        if self._asyncioByThread:
            self._asyncioByThread.shutdown(0.1)
            self._asyncioByThread = None
        if self._asyncioByTimer:
            self._asyncioByTimer.shutdown(0.1)
            self._asyncioByTimer = None
        self._shutdown_called = False

    def setUseDedicatedThread(self, use_dedicated_thread: bool) -> None:
        """Set whether to use dedicated thread for event loop"""
        if self._asyncioByThread is not None or self._asyncioByTimer is not None:
            raise InitializationError("Cannot change thread mode after initialization")
        self._use_dedicated_thread = use_dedicated_thread

    def __enter__(self):
        self._internal_enter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._internal_exit(exc_type, exc_value, traceback)

    def _internal_enter(self):
        """Initialize the asyncio integration"""
        logging.debug('Entering AsyncioPySide6')
        
        if self._asyncioByThread is not None or self._asyncioByTimer is not None:
            raise InitializationError("AsyncioPySide6 was already initialized. Please ensure proper cleanup before re-initialization.")

        if self._shutdown_called:
            raise InitializationError("Cannot reinitialize after shutdown")

        try:
            # Start asyncio event loop
            if self._use_dedicated_thread:
                self._asyncioByThread = AsyncioByThread()
                self._asyncioByThread.run_event_loop()
            else:
                self._asyncioByTimer = AsyncioByTimer()
                self._asyncioByTimer.run_event_loop()
        except Exception as e:
            logging.error(f"Failed to initialize AsyncioPySide6: {e}")
            raise InitializationError(f"Failed to initialize AsyncioPySide6: {e}")

    def _internal_exit(self, exc_type=None, exc_value=None, traceback=None):
        """Cleanup the asyncio integration"""
        logging.debug('Exiting AsyncioPySide6')
        self._internal_shutdown()

    def _internal_shutdown(self, timeout: float = None) -> bool:
        """Internal shutdown method"""
        try:
            config = get_config()
            if timeout is None:
                timeout = config.shutdown_timeout
                
            if self._asyncioByThread:
                success = self._asyncioByThread.shutdown(timeout)
                self._asyncioByThread = None
                if not success:
                    logging.warning("Thread shutdown may not have completed successfully")
                    
            if self._asyncioByTimer:
                success = self._asyncioByTimer.shutdown(timeout)
                self._asyncioByTimer = None
                if not success:
                    logging.warning("Timer shutdown may not have completed successfully")
                    
            self._shutdown_called = True
            return True
        except Exception as e:
            logging.error(f"Error during shutdown: {e}")
            return False

    def _internal_runTask(self, coro: Coroutine[Any, Any, Any]) -> None:
        """Run an asynchronous task in the appropriate event loop"""
        try:
            if self._use_dedicated_thread and self._asyncioByThread:
                loop = self._asyncioByThread.loop
            elif not self._use_dedicated_thread and self._asyncioByTimer:
                loop = self._asyncioByTimer.loop
            else:
                raise EventLoopError("Event loop not initialized")
                
            if loop and not loop.is_closed():
                # Create a future to handle the coroutine properly
                future = asyncio.run_coroutine_threadsafe(coro, loop)
                # Add a callback to handle any exceptions
                future.add_done_callback(self._handle_task_completion)
            else:
                raise EventLoopError("Event loop is closed or not available")
        except Exception as e:
            logging.error(f"Failed to run task: {e}")
            raise EventLoopError(f"Failed to run task: {e}")

    def _handle_task_completion(self, future):
        """Handle task completion and any exceptions"""
        try:
            # Get the result to ensure any exceptions are raised
            future.result()
        except Exception as e:
            logging.error(f"Task completed with error: {e}")
            # Don't re-raise here as this is called from a callback

    @staticmethod
    def use_asyncio(use_dedicated_thread: bool = None) -> 'AsyncioPySide6':
        """Get the singleton instance with specified thread mode"""
        instance = AsyncioPySide6()
        if use_dedicated_thread is not None:
            instance.setUseDedicatedThread(use_dedicated_thread)
        return instance

    @staticmethod
    def initialize(use_dedicated_thread: bool = None) -> None:
        """Initialize the AsyncioPySide6 object"""
        instance = AsyncioPySide6()
        if use_dedicated_thread is not None:
            instance.setUseDedicatedThread(use_dedicated_thread)
        instance._internal_enter()
            
    @staticmethod
    def dispose() -> bool:
        """Dispose of the AsyncioPySide6 object"""
        instance = AsyncioPySide6()
        return instance._internal_shutdown()

    @staticmethod
    def runTask(coro: Coroutine[Any, Any, Any]) -> None:
        """
        Run an asynchronous task in a separate thread.

        :param coro: Asynchronous coroutine to be executed.
        :raises EventLoopError: If the event loop is not available or task execution fails.
        """
        instance = AsyncioPySide6()
        instance._internal_runTask(coro)

    @staticmethod
    def create_and_run_task(coro_func: Callable[[], Coroutine[Any, Any, Any]]) -> None:
        """
        Create and run an asynchronous task in a separate thread.
        This method helps prevent RuntimeWarnings by ensuring the coroutine is created
        at the right time.

        :param coro_func: Function that returns an asynchronous coroutine to be executed.
        :raises EventLoopError: If the event loop is not available or task execution fails.
        """
        instance = AsyncioPySide6()
        coro = coro_func()
        instance._internal_runTask(coro)

    @staticmethod
    def run_task_safely(coro_func: Callable[[], Coroutine[Any, Any, Any]]) -> None:
        """
        Run an asynchronous task safely, preventing RuntimeWarnings.
        This is the recommended method for running tasks.

        :param coro_func: Function that returns an asynchronous coroutine to be executed.
        :raises EventLoopError: If the event loop is not available or task execution fails.
        """
        try:
            instance = AsyncioPySide6()
            coro = coro_func()
            instance._internal_runTask(coro)
        except Exception as e:
            logging.error(f"Failed to run task safely: {e}")
            raise EventLoopError(f"Failed to run task safely: {e}")

    @staticmethod
    def run_task_without_warnings(coro_func: Callable[[], Coroutine[Any, Any, Any]]) -> None:
        """
        Run an asynchronous task without RuntimeWarnings.
        This method suppresses coroutine warnings for testing purposes.

        :param coro_func: Function that returns an asynchronous coroutine to be executed.
        :raises EventLoopError: If the event loop is not available or task execution fails.
        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            try:
                instance = AsyncioPySide6()
                coro = coro_func()
                instance._internal_runTask(coro)
            except Exception as e:
                logging.error(f"Failed to run task without warnings: {e}")
                raise EventLoopError(f"Failed to run task without warnings: {e}")

    @staticmethod
    def invokeInGuiThread(gui_object: QObject, callable: Callable[[], None]) -> None:
        """
        Invoke a callable in the GUI thread.

        :param gui_object: QObject in which the callable will be executed.
        :param callable: Callable to be invoked in the GUI thread.
        :raises ThreadSafetyError: If the callable cannot be invoked safely.
        """
        try:
            QTimer.singleShot(0, gui_object, lambda: callable())
        except Exception as e:
            logging.error(f"Failed to invoke in GUI thread: {e}")
            raise ThreadSafetyError(f"Failed to invoke in GUI thread: {e}")

    @staticmethod
    def is_initialized() -> bool:
        """Check if AsyncioPySide6 is currently initialized"""
        instance = AsyncioPySide6()
        return (instance._asyncioByThread is not None or 
                instance._asyncioByTimer is not None)

    @staticmethod
    def shutdown(timeout: float = None) -> bool:
        """Shutdown AsyncioPySide6 with timeout"""
        instance = AsyncioPySide6()
        return instance._internal_shutdown(timeout)
    
    @staticmethod
    def reset_for_testing():
        """Reset the singleton for testing purposes"""
        instance = AsyncioPySide6()
        instance._reset_state()

    @staticmethod
    def runTaskWithTimeout(coro: Coroutine[Any, Any, Any], timeout: float = None) -> None:
        """
        Run an asynchronous task with timeout.
        
        :param coro: Asynchronous coroutine to be executed.
        :param timeout: Timeout in seconds. If None, uses default from config.
        :raises TaskTimeoutError: If the task exceeds the timeout.
        :raises EventLoopError: If the event loop is not available or task execution fails.
        """
        instance = AsyncioPySide6()
        config = get_config()
        if timeout is None:
            timeout = config.task_timeout
        
        task_id = str(uuid.uuid4())
        record_task_start(task_id)
        
        try:
            # Create a timeout wrapper
            async def timeout_wrapper():
                try:
                    return await asyncio.wait_for(coro, timeout=timeout)
                except asyncio.TimeoutError:
                    raise TaskTimeoutError(f"Task exceeded timeout of {timeout} seconds")
            
            instance._internal_runTask(timeout_wrapper())
            record_task_completion(task_id, True)
        except Exception as e:
            record_task_completion(task_id, False, str(e))
            raise

    @staticmethod
    def runTaskWithRetry(coro_func: Callable[[], Coroutine[Any, Any, Any]], 
                        max_retries: int = None, 
                        retry_delay: float = None) -> None:
        """
        Run an asynchronous task with retry logic.
        
        :param coro_func: Function that returns an asynchronous coroutine to be executed.
        :param max_retries: Maximum number of retry attempts. If None, uses default from config.
        :param retry_delay: Delay between retries in seconds. If None, uses default from config.
        :raises TaskExecutionError: If all retry attempts fail.
        :raises EventLoopError: If the event loop is not available or task execution fails.
        """
        instance = AsyncioPySide6()
        config = get_config()
        if max_retries is None:
            max_retries = config.max_retries
        if retry_delay is None:
            retry_delay = config.retry_delay
        
        task_id = str(uuid.uuid4())
        record_task_start(task_id)
        
        async def retry_wrapper():
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    coro = coro_func()
                    return await coro
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        await asyncio.sleep(retry_delay)
                    else:
                        raise TaskExecutionError(f"Task failed after {max_retries + 1} attempts: {e}")
        
        try:
            instance._internal_runTask(retry_wrapper())
            record_task_completion(task_id, True)
        except Exception as e:
            record_task_completion(task_id, False, str(e))
            raise

    @staticmethod
    def runTaskWithProgress(coro: Coroutine[Any, Any, Any], 
                          progress_callback: Callable[[float], None]) -> None:
        """
        Run an asynchronous task with progress reporting.
        
        :param coro: Asynchronous coroutine to be executed.
        :param progress_callback: Callback function for progress updates (0.0 to 1.0).
        :raises EventLoopError: If the event loop is not available or task execution fails.
        """
        instance = AsyncioPySide6()
        task_id = str(uuid.uuid4())
        record_task_start(task_id)
        
        async def progress_wrapper():
            try:
                # For now, we'll just call the progress callback at start and end
                # In a real implementation, the coroutine would need to support progress reporting
                progress_callback(0.0)
                result = await coro
                progress_callback(1.0)
                return result
            except Exception as e:
                progress_callback(1.0)  # Indicate completion even on error
                raise
        
        try:
            instance._internal_runTask(progress_wrapper())
            record_task_completion(task_id, True)
        except Exception as e:
            record_task_completion(task_id, False, str(e))
            raise

    @staticmethod
    def get_health_status() -> dict:
        """
        Get the current health status of the system.
        
        :return: Dictionary containing health status information.
        """
        return get_health_status()

    @staticmethod
    def cleanup_resources() -> None:
        """
        Clean up resources and perform garbage collection.
        This method helps prevent memory leaks.
        """
        import gc
        gc.collect()
        logging.info("Resource cleanup completed")

    @staticmethod
    def get_task_count() -> int:
        """
        Get the current number of active tasks.
        
        :return: Number of active tasks.
        """
        instance = AsyncioPySide6()
        if instance._use_dedicated_thread and instance._asyncioByThread:
            loop = instance._asyncioByThread.loop
        elif not instance._use_dedicated_thread and instance._asyncioByTimer:
            loop = instance._asyncioByTimer.loop
        else:
            return 0
        
        if loop and not loop.is_closed():
            return len(asyncio.all_tasks(loop))
        return 0