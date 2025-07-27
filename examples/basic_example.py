#!/usr/bin/env python3
"""
Basic Example - pyside6-asyncplus with QtAsyncio Integration.

This example demonstrates the basic usage of pyside6-asyncplus with QtAsyncio integration.
It shows how to run simple async tasks, handle timeouts, and use retry logic.
"""

import asyncio
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QTextEdit
from PySide6.QtCore import QTimer

# Import our enhanced pyside6-asyncplus
sys.path.append('..')
from pyside6_asyncplus.app import app as async_app, run, run_with_timeout, run_with_retry, invoke_in_gui_thread


class BasicExample(QMainWindow):
    """
    Basic example demonstrating pyside6-asyncplus with QtAsyncio integration.
    
    This example shows:
    - Basic async task execution
    - Timeout handling
    - Retry logic
    - GUI thread safety
    """
    
    def __init__(self):
        """Initialize the basic example window."""
        super().__init__()
        self.setWindowTitle("pyside6-asyncplus Basic Example")
        self.setGeometry(100, 100, 600, 400)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create UI elements
        self.status_label = QLabel("Status: Ready")
        layout.addWidget(self.status_label)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        layout.addWidget(self.log_text)
        
        # Create buttons
        self.basic_task_btn = QPushButton("Run Basic Task")
        self.basic_task_btn.clicked.connect(self.run_basic_task)
        layout.addWidget(self.basic_task_btn)
        
        self.timeout_task_btn = QPushButton("Run Task with Timeout")
        self.timeout_task_btn.clicked.connect(self.run_timeout_task)
        layout.addWidget(self.timeout_task_btn)
        
        self.retry_task_btn = QPushButton("Run Task with Retry")
        self.retry_task_btn.clicked.connect(self.run_retry_task)
        layout.addWidget(self.retry_task_btn)
        
        # Add a timer to demonstrate the event loop is working
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Update every second
        self.timer_count = 0
    
    def log(self, message: str):
        """Add message to log with timestamp.
        
        Args:
            message: The message to log
        """
        self.log_text.append(f"[{self.timer_count}s] {message}")
    
    def update_timer(self):
        """Update timer counter to show event loop is working."""
        self.timer_count += 1
        self.status_label.setText(f"Status: Timer running ({self.timer_count}s)")
    
    async def basic_async_task(self):
        """Basic async task that simulates some work.
        
        Returns:
            str: Result message
        """
        self.log("Starting basic async task...")
        await asyncio.sleep(2)  # Simulate work
        self.log("Basic async task completed!")
        return "Basic task completed successfully"
    
    async def timeout_async_task(self):
        """Async task that takes longer than the timeout.
        
        This task will timeout because it takes 5 seconds but the timeout is 3 seconds.
        
        Returns:
            str: Result message
        """
        self.log("Starting timeout async task...")
        await asyncio.sleep(5)  # This will timeout
        self.log("Timeout async task completed!")
        return "Timeout task completed successfully"
    
    async def retry_async_task(self):
        """Async task that might fail and need retry.
        
        This task simulates a flaky operation that might fail.
        
        Returns:
            str: Result message
        """
        import random
        self.log("Starting retry async task...")
        
        # Simulate random failure (70% chance of failure)
        if random.random() < 0.7:
            raise Exception("Random failure in retry task")
        
        await asyncio.sleep(1)
        self.log("Retry async task completed!")
        return "Retry task completed successfully"
    
    def run_basic_task(self):
        """Run a basic async task."""
        self.log("=== Running Basic Task ===")
        self.status_label.setText("Status: Running basic task...")
        
        def update_gui():
            """Update GUI after task completion."""
            self.status_label.setText("Status: Basic task completed!")
            self.log("GUI updated: Basic task completed!")
        
        # Run the task using pyside6-asyncplus
        run(self.basic_async_task())
        
        # Update GUI after task
        invoke_in_gui_thread(self, update_gui)
    
    def run_timeout_task(self):
        """Run a task with timeout handling."""
        self.log("=== Running Timeout Task ===")
        self.status_label.setText("Status: Running timeout task...")
        
        def update_gui():
            """Update GUI after task completion."""
            self.status_label.setText("Status: Timeout task completed!")
            self.log("GUI updated: Timeout task completed!")
        
        # Run the task with timeout (3 seconds)
        run_with_timeout(self.timeout_async_task(), 3.0)
        
        # Update GUI after task
        invoke_in_gui_thread(self, update_gui)
    
    def run_retry_task(self):
        """Run a task with retry logic."""
        self.log("=== Running Retry Task ===")
        self.status_label.setText("Status: Running retry task...")
        
        def update_gui():
            """Update GUI after task completion."""
            self.status_label.setText("Status: Retry task completed!")
            self.log("GUI updated: Retry task completed!")
        
        # Run the task with retry logic (3 retries, 1 second delay)
        run_with_retry(
            lambda: self.retry_async_task(),
            max_retries=3,
            retry_delay=1.0
        )
        
        # Update GUI after task
        invoke_in_gui_thread(self, update_gui)


def main():
    """Main function to run the basic example."""
    app = QApplication(sys.argv)
    
    # Create and show the example window
    example = BasicExample()
    example.show()
    
    # Run the application with pyside6-asyncplus
    with async_app:
        sys.exit(app.exec())


if __name__ == "__main__":
    main() 