# AsyncioPySide6
Empower Qt PySide6 developers with seamless async/await asynchronous programming capabilities

Installation:
```
pip install AsyncioPySide6
```

Example:
```python
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel
from AsyncioPySide6 import AsyncioPySide6
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

        # Execute an asynchronous task
        AsyncioPySide6.runTask(self.calculate_async(20))

    def init_ui(self):
        """Initialize GUI"""
        self.label = QLabel("Calculating...")
        self.setCentralWidget(self.label)
    
    async def calculate_async(self, n:int):
        """Asynchronous method that does a time-expensive calculation"""
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
        """Updated GUI label, it must be ran in GUI thread"""
        self.label.setText(text)

if __name__ == "__main__":
    with AsyncioPySide6():
        if not QApplication.instance():
            app = QApplication(sys.argv)
            main_window = MainWindow()
            main_window.show()
            app.exec()
```