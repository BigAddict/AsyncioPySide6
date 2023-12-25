import asyncio
import logging
import time
import typing

from PySide6.QtCore import QThread, QObject, QTimer

class AsyncioThread(QThread):
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
     
    _thread: AsyncioThread = None

    def __init__(self):
        """Only create an AsyncioPySide6 object if you are using "with" keyword"""
        pass

    def __enter__(self):
        AsyncioPySide6.init()

    def __exit__(self, exc_type, exc_value, traceback):
        AsyncioPySide6.dispose()

    @staticmethod
    def init():
        """Initialize the AsyncioPySide6 object"""

        logging.debug('Entering AsyncioUtils')
        assert (AsyncioPySide6._thread is None), "AsyncioPySide6 was entered multiple-times. Please make sure the AsyncioPySide6.init() method is called at most once."

        # Start asyncio event loop thread
        AsyncioPySide6._thread = AsyncioThread()
        thread = AsyncioPySide6._thread
        thread.start()

        # Wait until the asyncio event loop is created
        while (thread.loop is None):
            time.sleep(0.01)

    @staticmethod
    def runTask(coro: typing.Coroutine):
        """
        Run an asynchronous task in a separate thread.

        :param coro: Asynchronous coroutine to be executed.
        """

        #AsyncioUtils._thread.loop.run_until_complete(coro)
        loop = AsyncioPySide6._thread.loop
        asyncio.run_coroutine_threadsafe(coro, loop)


    @staticmethod
    def dispose():
        logging.debug('Exiting AsyncioUtils')
        if (AsyncioPySide6._thread):
            AsyncioPySide6._thread.isShuttingDown = True
            AsyncioPySide6._thread.wait(10 * 1000)
            AsyncioPySide6._thread = None

    @staticmethod
    def invokeInGuiThread(gui_object:QObject, callable: typing.Callable[[], None]):
        """
        Invoke a callable in the GUI thread.

        :param gui_object: QObject in which the callable will be executed.
        :param callable: Callable to be invoked in the GUI thread.
        """        
        QTimer.singleShot(0, gui_object, lambda: callable())
