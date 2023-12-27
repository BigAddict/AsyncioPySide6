import unittest
import asyncio
import time
from AsyncioPySide6.nvd.AsyncioPySide6 import AsyncioPySide6


from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QMessageBox
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.label = QLabel("Calculating...")
        self.setCentralWidget(self.label)

        # Execute the asynchronous task
        AsyncioPySide6.runTask(self.calculate_async(20))

    async def calculate_async(self, n:int):
        # Give Qt sometime to show the window
        await asyncio.sleep(0.5)

        # Calculate
        sum = 0
        for i in range(n):
            # Create some delay
            await asyncio.sleep(0.1)

            sum = sum + i
            AsyncioPySide6.invokeInGuiThread(self, lambda: self._update_label(f"SUM([0..{i}]) = {sum}"))

    def _update_label(self, text):
        self.label.setText(text)


import sys
class TestAsyncioPySide6(unittest.TestCase):
    @unittest.skipIf(not ("--AsyncioPySide6-gui-test" in sys.argv), reason="This test show GUI window")
    def test_runGUITask(self):
        if not QApplication.instance():
            app = QApplication(sys.argv)
        else:
            app = QApplication.instance()
        with AsyncioPySide6():
            main_window = MainWindow()
            main_window.show()

    def test_runConsoleTask(self):
        async def calculate_async(n:int):
            # Give Qt sometime to show the window
            await asyncio.sleep(0.5)

            # Calculate
            sum = 0
            for i in range(n):
                # Create some delay
                await asyncio.sleep(0.1)

                sum = sum + i
                print(f"SUM([0..{i}]) = {sum}")

        if not QApplication.instance():
            app = QApplication(sys.argv)
        else:
            app = QApplication.instance()
        with AsyncioPySide6.use_asyncio(use_dedicated_thread=True):
            AsyncioPySide6.runTask(calculate_async(10))
            time.sleep(2)

        with AsyncioPySide6.use_asyncio(use_dedicated_thread=False):
            AsyncioPySide6.runTask(calculate_async(10))
            QMessageBox.critical(None, 'Testing', 'Close this when it is done')