import asyncio
import logging
import time
import typing

from PySide6.QtCore import QThread, QObject, QTimer

class AsyncioByThread(QThread):
    def __init__(self):
        super().__init__()
        self.isShuttingDown = False
        self.loop:asyncio.AbstractEventLoop = None

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._event_loop())

    async def _event_loop(self):
        while not self.isShuttingDown:
            await asyncio.sleep(1)

    def run_event_loop(self):
        self.start()
        # Wait until the asyncio event loop is created
        while (self.loop is None):
            time.sleep(0.01)

    def shutdown(self):
        self.isShuttingDown = True
        self.wait(10 * 1000)


class AsyncioByTimer(QTimer):
    def __init__(self):
        super().__init__()
       
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.isShuttingDown = False
        self.timeout.connect(self._timer_timemout)
        self.setInterval(10)        


    def _timer_timemout(self):
        self.loop.run_until_complete(self._event_loop())

    async def _event_loop(self):
        await asyncio.sleep(1)

    def run_event_loop(self):
        self.start()

    def shutdown(self):
        self.isShuttingDown = True
        self.stop()

USE_DEDICATED_THREAD_DEFAULT_VALUE = True

class AsyncioPySide6:
    """
    A utility class to simplify integration of asynchronous programming with Qt PySide6 projects.

    Usage:
    ```
    with AsyncioPySide6():
        # Your Qt PySide6 application code here
    ```

    Alternatively, you can use `AsyncioPySide6.init()` and `AsyncioPySide6.dispose()` if the "with" statement is not preferred.
    """
    _singleton:'AsyncioPySide6' = None

    def __init__(self):
        assert (AsyncioPySide6._singleton is None), "AsyncioPySide6 is instantiated multiple times. The constructor is not supposed to be called directly by the client!!!"
        self._asyncioByThread: AsyncioByThread = None
        self._asyncioByTimer: AsyncioByTimer = None
        self._use_dedicated_thread: False
        pass


    def setUseDedicatedThread(self, use_dedicated_thread:bool):
        self._use_dedicated_thread = use_dedicated_thread
        

    def __enter__(self):
        self._internal_enter()

    def __exit__(self, exc_type, exc_value, traceback):
        self._internal_exit(exc_type, exc_value, traceback)


    def _internal_enter(self):
        logging.debug('Entering AsyncioPySide6')
        assert (self._asyncioByThread is None) and (self._asyncioByTimer is None), "AsyncioPySide6 was entered multiple-times. Please make sure the AsyncioPySide6.initialize() method is called at most once."

        # Start asyncio event loop
        obj = AsyncioPySide6._singleton
        if self._use_dedicated_thread:
            self._asyncioByThread = AsyncioByThread()
            self._asyncioByThread.run_event_loop()
        else:
            self._asyncioByTimer = AsyncioByTimer()
            self._asyncioByTimer.run_event_loop()
            pass

    def _internal_exit(self, exc_type = None, exc_value = None, traceback = None):
        logging.debug('Exiting AsyncioPySide6')
        if (self._asyncioByThread):
            self._asyncioByThread.shutdown()
            self._asyncioByThread = None
        if (self._asyncioByTimer):
            self._asyncioByTimer.shutdown()
            self._asyncioByTimer = None

    def _internal_runTask(self, coro:typing.Coroutine):
        #AsyncioUtils._thread.loop.run_until_complete(coro)
        if self._use_dedicated_thread:
            loop = self._asyncioByThread.loop
        else:
            loop = self._asyncioByTimer.loop
        asyncio.run_coroutine_threadsafe(coro, loop)



    @staticmethod
    def use_asyncio(use_dedicated_thread=USE_DEDICATED_THREAD_DEFAULT_VALUE):
        AsyncioPySide6._singleton.setUseDedicatedThread(use_dedicated_thread)
        return AsyncioPySide6._singleton

    @staticmethod
    def initialize(use_dedicated_thread=USE_DEDICATED_THREAD_DEFAULT_VALUE):
        """Initialize the AsyncioPySide6 object"""
        AsyncioPySide6._singleton.setUseDedicatedThread(use_dedicated_thread)
        AsyncioPySide6._singleton._internal_enter()
            
    @staticmethod
    def dispose():
        AsyncioPySide6._singleton._internal_exit()

    @staticmethod
    def runTask(coro: typing.Coroutine):
        """
        Run an asynchronous task in a separate thread.

        :param coro: Asynchronous coroutine to be executed.
        """
        AsyncioPySide6._singleton._internal_runTask(coro)

    @staticmethod
    def invokeInGuiThread(gui_object:QObject, callable: typing.Callable[[], None]):
        """
        Invoke a callable in the GUI thread.

        :param gui_object: QObject in which the callable will be executed.
        :param callable: Callable to be invoked in the GUI thread.
        """        
        QTimer.singleShot(0, gui_object, lambda: callable())

AsyncioPySide6._singleton = AsyncioPySide6()