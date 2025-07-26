#!/usr/bin/env python3
"""
Basic AsyncioPySide6 Usage Example

This example shows the basic usage of the library with the new Phase 1 features.
"""

import sys
import asyncio
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from AsyncioPySide6 import AsyncioPySide6

class BasicMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

        # Execute an asynchronous task
        AsyncioPySide6.runTask(self.calculate_async(20))

    def init_ui(self):
        """Initialize GUI"""
        self.setWindowTitle("AsyncioPySide6 Basic Demo")
        self.setGeometry(100, 100, 400, 200)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Create label
        self.label = QLabel("Calculating...")
        layout.addWidget(self.label)
    
    async def calculate_async(self, n: int):
        """Asynchronous method that does a time-expensive calculation"""
        # Give Qt some time to show the window
        await asyncio.sleep(0.5)

        # Calculate
        sum = 0
        for i in range(n):
            # Create some delay
            await asyncio.sleep(0.1)

            sum = sum + i
            self.label.setText(f"SUM([0..{i}]) = {sum}")

        self.label.setText(f"Final result: {sum}")


def main():
    """Main function with error handling"""
    app = QApplication(sys.argv)
    
    try:
        # Use the library with context manager
        with AsyncioPySide6.use_asyncio():
            main_window = BasicMainWindow()
            main_window.show()
            return app.exec()
            
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 