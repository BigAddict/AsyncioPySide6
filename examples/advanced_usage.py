#!/usr/bin/env python3
"""
Advanced AsyncioPySide6 Usage Example

This example demonstrates the new Phase 1 features including:
- Configuration system
- Error handling
- Environment variables
- Production-ready features
"""

import sys
import asyncio
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QTextEdit
from PySide6.QtCore import QTimer
from AsyncioPySide6 import AsyncioPySide6, get_config, set_config, AsyncioPySide6Error, EventLoopError

class AdvancedMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_configuration()
        
        # Execute multiple asynchronous tasks
        self.run_demo_tasks()

    def init_ui(self):
        """Initialize GUI with multiple components"""
        self.setWindowTitle("AsyncioPySide6 Advanced Demo")
        self.setGeometry(100, 100, 600, 400)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Create UI components
        self.status_label = QLabel("Status: Initializing...")
        self.result_label = QLabel("Results: ")
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        
        # Add components to layout
        layout.addWidget(self.status_label)
        layout.addWidget(self.result_label)
        layout.addWidget(self.log_text)
        
        # Add control buttons
        self.start_button = QPushButton("Start Tasks")
        self.start_button.clicked.connect(self.run_demo_tasks)
        layout.addWidget(self.start_button)
        
        self.config_button = QPushButton("Show Config")
        self.config_button.clicked.connect(self.show_configuration)
        layout.addWidget(self.config_button)

    def setup_configuration(self):
        """Demonstrate configuration system"""
        try:
            # Get current configuration
            config = get_config()
            
            # Modify configuration for this demo
            config.event_loop_interval = 0.005  # Faster processing
            config.shutdown_timeout = 15.0      # Longer shutdown timeout
            config.enable_debug_mode = True     # Enable debug logging
            config.log_level = "DEBUG"          # More detailed logging
            
            # Apply configuration
            set_config(config)
            
            self.log_message("Configuration applied successfully")
            
        except AsyncioPySide6Error as e:
            self.log_message(f"Configuration error: {e}")

    def log_message(self, message: str):
        """Add message to log display"""
        try:
            loop = asyncio.get_event_loop()
            timestamp = loop.time() if loop.is_running() else 0.0
            self.log_text.append(f"[{timestamp:.2f}] {message}")
        except Exception:
            # Fallback if event loop is not available
            self.log_text.append(f"[{message}]")

    def show_configuration(self):
        """Display current configuration"""
        try:
            config = get_config()
            config_str = str(config)
            self.log_message("Current Configuration:")
            self.log_message(config_str)
        except AsyncioPySide6Error as e:
            self.log_message(f"Error getting config: {e}")

    def run_demo_tasks(self):
        """Run multiple demo tasks with error handling"""
        self.status_label.setText("Status: Running tasks...")
        self.start_button.setEnabled(False)
        
        # Task 1: Basic calculation
        AsyncioPySide6.runTask(self.calculate_async(10))
        
        # Task 2: Error handling demo
        AsyncioPySide6.runTask(self.error_handling_demo())
        
        # Task 3: Configuration demo
        AsyncioPySide6.runTask(self.configuration_demo())
        
        # Task 4: Performance demo
        AsyncioPySide6.runTask(self.performance_demo())

    async def calculate_async(self, n: int):
        """Basic calculation task"""
        try:
            self.log_message(f"Starting calculation for n={n}")
            
            sum = 0
            for i in range(n):
                await asyncio.sleep(0.2)  # Simulate work
                sum += i
                self.result_label.setText(f"SUM([0..{i}]) = {sum}")
                self.log_message(f"Progress: {i+1}/{n}")
            
            self.log_message(f"Calculation completed: {sum}")
            self.status_label.setText("Status: Calculation completed")
            
        except Exception as e:
            self.log_message(f"Calculation error: {e}")

    async def error_handling_demo(self):
        """Demonstrate error handling"""
        try:
            self.log_message("Starting error handling demo")
            
            # Simulate different types of errors
            await asyncio.sleep(1.0)
            
            # This will be caught by the library's error handling
            raise RuntimeError("Simulated error for demo")
            
        except EventLoopError as e:
            self.log_message(f"Event loop error: {e}")
        except AsyncioPySide6Error as e:
            self.log_message(f"AsyncioPySide6 error: {e}")
        except Exception as e:
            self.log_message(f"General error: {e}")

    async def configuration_demo(self):
        """Demonstrate configuration changes"""
        try:
            self.log_message("Starting configuration demo")
            
            # Get current config
            config = get_config()
            self.log_message(f"Current event loop interval: {config.event_loop_interval}")
            
            # Temporarily change configuration
            original_interval = config.event_loop_interval
            config.event_loop_interval = 0.01
            set_config(config)
            self.log_message(f"Changed event loop interval to: {config.event_loop_interval}")
            
            await asyncio.sleep(2.0)
            
            # Restore original configuration
            config.event_loop_interval = original_interval
            set_config(config)
            self.log_message(f"Restored event loop interval to: {config.event_loop_interval}")
            
        except AsyncioPySide6Error as e:
            self.log_message(f"Configuration demo error: {e}")

    async def performance_demo(self):
        """Demonstrate performance features"""
        try:
            self.log_message("Starting performance demo")
            
            # Run multiple concurrent tasks
            tasks = []
            for i in range(5):
                task = asyncio.create_task(self.simple_task(i))
                tasks.append(task)
            
            # Wait for all tasks to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    self.log_message(f"Task {i} failed: {result}")
                else:
                    self.log_message(f"Task {i} completed: {result}")
            
            self.log_message("Performance demo completed")
            self.start_button.setEnabled(True)
            
        except Exception as e:
            self.log_message(f"Performance demo error: {e}")

    async def simple_task(self, task_id: int):
        """Simple task for performance demo"""
        await asyncio.sleep(0.5 + task_id * 0.1)
        return f"Task {task_id} result"


def main():
    """Main function demonstrating environment variable configuration"""
    
    # Set environment variables for configuration
    os.environ['ASYNCIOPYSIDE6_EVENT_LOOP_INTERVAL'] = '0.005'
    os.environ['ASYNCIOPYSIDE6_ENABLE_DEBUG_MODE'] = 'true'
    os.environ['ASYNCIOPYSIDE6_LOG_LEVEL'] = 'DEBUG'
    
    app = QApplication(sys.argv)
    
    try:
        # Use the library with error handling
        with AsyncioPySide6.use_asyncio(use_dedicated_thread=True):
            main_window = AdvancedMainWindow()
            main_window.show()
            
            # Set up a timer to update the status
            timer = QTimer()
            timer.timeout.connect(lambda: main_window.status_label.setText(
                f"Status: Running (Event Loop: {asyncio.get_event_loop().is_running()})"
            ))
            timer.start(1000)
            
            return app.exec()
            
    except AsyncioPySide6Error as e:
        print(f"Failed to initialize AsyncioPySide6: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 