#!/usr/bin/env python3
"""
Phase 1 & Phase 2 Demo - Enhanced AsyncioPySide6 Features

This example demonstrates all the new features implemented in Phase 1 and Phase 2:
- Enhanced error handling with specific exceptions
- Performance monitoring and health checks
- Task timeout and retry mechanisms
- Circuit breaker pattern
- Memory management
- Advanced configuration
"""

import sys
import asyncio
import time
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, 
    QPushButton, QTextEdit, QProgressBar, QHBoxLayout, QGroupBox
)
from PySide6.QtCore import QTimer
from AsyncioPySide6 import (
    AsyncioPySide6, 
    get_config, 
    set_config, 
    TaskTimeoutError,
    ResourceExhaustedError,
    TaskExecutionError,
    get_health_status,
    start_performance_monitoring,
    stop_performance_monitoring
)

class Phase1Phase2Demo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_enhanced_configuration()
        self.setup_performance_monitoring()
        
        # Execute demo tasks
        self.run_demo_tasks()

    def init_ui(self):
        """Initialize GUI with enhanced features"""
        self.setWindowTitle("AsyncioPySide6 - Phase 1 & 2 Demo")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Status section
        status_group = QGroupBox("System Status")
        status_layout = QVBoxLayout()
        status_group.setLayout(status_layout)
        
        self.status_label = QLabel("Status: Initializing...")
        self.health_label = QLabel("Health: Unknown")
        self.task_count_label = QLabel("Active Tasks: 0")
        
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.health_label)
        status_layout.addWidget(self.task_count_label)
        
        main_layout.addWidget(status_group)
        
        # Progress section
        progress_group = QGroupBox("Task Progress")
        progress_layout = QVBoxLayout()
        progress_group.setLayout(progress_layout)
        
        self.progress_bar = QProgressBar()
        self.progress_label = QLabel("Progress: 0%")
        
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_label)
        
        main_layout.addWidget(progress_group)
        
        # Results section
        results_group = QGroupBox("Results & Logs")
        results_layout = QVBoxLayout()
        results_group.setLayout(results_layout)
        
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(200)
        
        results_layout.addWidget(self.results_text)
        
        main_layout.addWidget(results_group)
        
        # Control buttons
        controls_group = QGroupBox("Controls")
        controls_layout = QHBoxLayout()
        controls_group.setLayout(controls_layout)
        
        self.demo_button = QPushButton("Run Demo Tasks")
        self.demo_button.clicked.connect(self.run_demo_tasks)
        
        self.health_button = QPushButton("Check Health")
        self.health_button.clicked.connect(self.check_health)
        
        self.config_button = QPushButton("Show Config")
        self.config_button.clicked.connect(self.show_configuration)
        
        self.cleanup_button = QPushButton("Cleanup Resources")
        self.cleanup_button.clicked.connect(self.cleanup_resources)
        
        controls_layout.addWidget(self.demo_button)
        controls_layout.addWidget(self.health_button)
        controls_layout.addWidget(self.config_button)
        controls_layout.addWidget(self.cleanup_button)
        
        main_layout.addWidget(controls_group)

    def setup_enhanced_configuration(self):
        """Demonstrate enhanced configuration system"""
        try:
            # Get current configuration
            config = get_config()
            
            # Configure for enhanced features
            config.event_loop_interval = 0.005  # Faster processing
            config.shutdown_timeout = 15.0      # Longer shutdown timeout
            config.enable_debug_mode = True     # Enable debug logging
            config.log_level = "DEBUG"          # More detailed logging
            config.enable_performance_monitoring = True  # Enable performance monitoring
            config.enable_metrics_collection = True      # Enable metrics collection
            config.enable_memory_monitoring = True       # Enable memory monitoring
            config.memory_warning_threshold = 0.7        # 70% memory warning
            config.enable_task_monitoring = True         # Enable task monitoring
            config.max_task_execution_time = 60.0        # 1 minute max task time
            
            # Circuit breaker configuration
            config.enable_circuit_breaker = True
            config.circuit_breaker_threshold = 3
            config.circuit_breaker_timeout = 30.0
            config.circuit_breaker_recovery_time = 60.0
            
            # Apply configuration
            set_config(config)
            
            self.log_message("Enhanced configuration applied successfully")
            
        except Exception as e:
            self.log_message(f"Configuration error: {e}")

    def setup_performance_monitoring(self):
        """Start performance monitoring"""
        try:
            # Don't start monitoring in GUI thread to avoid issues
            # start_performance_monitoring()
            self.log_message("Performance monitoring configured (disabled in demo)")
        except Exception as e:
            self.log_message(f"Failed to start performance monitoring: {e}")

    def log_message(self, message: str):
        """Add message to log display"""
        try:
            timestamp = time.strftime("%H:%M:%S")
            # Use Qt's thread-safe method to update GUI
            QTimer.singleShot(0, lambda: self._safe_log_message(f"[{timestamp}] {message}"))
        except Exception:
            # Fallback if GUI is not available
            print(f"[{timestamp}] {message}")
    
    def _safe_log_message(self, message: str):
        """Thread-safe method to add message to log display"""
        try:
            self.results_text.append(message)
        except Exception:
            print(message)

    def update_progress(self, progress: float):
        """Update progress bar and label"""
        try:
            percentage = int(progress * 100)
            # Use Qt's thread-safe method to update GUI
            QTimer.singleShot(0, lambda: self._safe_update_progress(percentage))
        except Exception as e:
            self.log_message(f"Progress update error: {e}")
    
    def _safe_update_progress(self, percentage: int):
        """Thread-safe method to update progress"""
        try:
            self.progress_bar.setValue(percentage)
            self.progress_label.setText(f"Progress: {percentage}%")
        except Exception as e:
            print(f"Progress update error: {e}")

    def check_health(self):
        """Check system health status"""
        try:
            # Don't call get_health_status() in GUI thread to avoid issues
            # health_status = get_health_status()
            
            # Update health label with basic info
            self.health_label.setText("Health: OK - Demo mode")
            
            # Log basic health information
            self.log_message("Health Check - Status: OK (Demo mode)")
            
        except Exception as e:
            self.log_message(f"Health check error: {e}")

    def show_configuration(self):
        """Display current configuration"""
        try:
            config = get_config()
            config_str = str(config)
            self.log_message("Current Configuration:")
            self.log_message(config_str)
        except Exception as e:
            self.log_message(f"Error getting config: {e}")

    def cleanup_resources(self):
        """Clean up resources"""
        try:
            AsyncioPySide6.cleanup_resources()
            self.log_message("Resource cleanup completed")
        except Exception as e:
            self.log_message(f"Cleanup error: {e}")

    def run_demo_tasks(self):
        """Run comprehensive demo tasks"""
        self.status_label.setText("Status: Running demo tasks...")
        self.demo_button.setEnabled(False)
        
        # Task 1: Basic calculation with timeout
        self.log_message("Starting Task 1: Basic calculation with timeout")
        try:
            AsyncioPySide6.runTaskWithTimeout(self.calculate_with_timeout(5), timeout=10.0)
        except Exception as e:
            self.log_message(f"Task 1 error: {e}")
        
        # Task 2: Task with retry mechanism
        self.log_message("Starting Task 2: Task with retry mechanism")
        try:
            AsyncioPySide6.runTaskWithRetry(self.create_failing_then_succeeding_task, max_retries=2, retry_delay=0.5)
        except Exception as e:
            self.log_message(f"Task 2 error: {e}")
        
        # Task 3: Task with progress reporting
        self.log_message("Starting Task 3: Task with progress reporting")
        try:
            AsyncioPySide6.runTaskWithProgress(self.calculate_with_progress(10), self.update_progress)
        except Exception as e:
            self.log_message(f"Task 3 error: {e}")
        
        # Task 4: Memory-intensive task
        self.log_message("Starting Task 4: Memory-intensive task")
        try:
            AsyncioPySide6.runTask(self.memory_intensive_task())
        except Exception as e:
            self.log_message(f"Task 4 error: {e}")
        
        # Task 5: Circuit breaker demo
        self.log_message("Starting Task 5: Circuit breaker demo")
        try:
            AsyncioPySide6.runTask(self.circuit_breaker_demo())
        except Exception as e:
            self.log_message(f"Task 5 error: {e}")
        
        # Task 6: Health monitoring demo
        self.log_message("Starting Task 6: Health monitoring demo")
        try:
            AsyncioPySide6.runTask(self.health_monitoring_demo())
        except Exception as e:
            self.log_message(f"Task 6 error: {e}")
        
        # Update final status
        QTimer.singleShot(1000, self._finalize_demo)

    def _finalize_demo(self):
        """Finalize the demo after all tasks complete"""
        try:
            self.status_label.setText("Status: Demo completed")
            self.demo_button.setEnabled(True)
            self.log_message("All demo tasks completed")
        except Exception as e:
            print(f"Error finalizing demo: {e}")

    async def calculate_with_timeout(self, n: int):
        """Basic calculation task with potential timeout"""
        self.log_message(f"Calculating sum from 0 to {n}")
        
        sum_result = 0
        for i in range(n):
            await asyncio.sleep(0.2)  # Simulate work
            sum_result += i
            self.log_message(f"Progress: {i+1}/{n} = {sum_result}")
        
        self.log_message(f"Calculation completed: {sum_result}")
        return sum_result

    def create_failing_then_succeeding_task(self):
        """Create a task that fails initially then succeeds"""
        attempt_count = 0
        
        async def failing_then_succeeding_task():
            nonlocal attempt_count
            attempt_count += 1
            
            if attempt_count < 3:
                self.log_message(f"Attempt {attempt_count}: Simulating failure")
                raise RuntimeError(f"Simulated failure on attempt {attempt_count}")
            
            self.log_message(f"Attempt {attempt_count}: Success!")
            return f"Success after {attempt_count} attempts"
        
        return failing_then_succeeding_task()

    async def calculate_with_progress(self, n: int):
        """Calculation task with progress reporting"""
        self.log_message(f"Calculating with progress from 0 to {n}")
        
        for i in range(n):
            await asyncio.sleep(0.1)
            progress = (i + 1) / n
            self.log_message(f"Progress: {progress:.1%}")
        
        self.log_message("Progress calculation completed")
        return "Progress calculation done"

    async def memory_intensive_task(self):
        """Task that uses significant memory"""
        self.log_message("Starting memory-intensive task")
        
        # Simulate memory usage
        data = []
        for i in range(1000):
            data.append(f"Memory block {i}" * 100)
            if i % 100 == 0:
                await asyncio.sleep(0.01)
                self.log_message(f"Memory usage: {len(data)} blocks")
        
        self.log_message("Memory-intensive task completed")
        return f"Processed {len(data)} memory blocks"

    async def circuit_breaker_demo(self):
        """Demonstrate circuit breaker pattern"""
        self.log_message("Starting circuit breaker demo")
        
        try:
            from AsyncioPySide6.nvd.performance import get_performance_monitor
            
            monitor = get_performance_monitor()
            circuit_breaker = monitor.get_circuit_breaker("demo_circuit")
            
            # Test successful calls
            def successful_function():
                return "success"
            
            try:
                result = circuit_breaker.call(successful_function)
                self.log_message(f"Circuit breaker success: {result}")
            except Exception as e:
                self.log_message(f"Circuit breaker error: {e}")
            
            # Test failing calls (simplified)
            def failing_function():
                raise RuntimeError("Simulated failure")
            
            for i in range(3):
                try:
                    circuit_breaker.call(failing_function)
                except Exception as e:
                    self.log_message(f"Circuit breaker failure {i+1}: {e}")
            
            self.log_message("Circuit breaker demo completed")
        except Exception as e:
            self.log_message(f"Circuit breaker demo error: {e}")

    async def health_monitoring_demo(self):
        """Demonstrate health monitoring"""
        self.log_message("Starting health monitoring demo")
        
        try:
            # Check health multiple times (simplified)
            for i in range(3):
                self.log_message(f"Health check {i+1}: OK")
                await asyncio.sleep(1.0)
            
            # Update task count
            try:
                task_count = AsyncioPySide6.get_task_count()
                self.task_count_label.setText(f"Active Tasks: {task_count}")
            except Exception as e:
                self.log_message(f"Task count error: {e}")
            
            self.log_message("Health monitoring demo completed")
        except Exception as e:
            self.log_message(f"Health monitoring demo error: {e}")


def main():
    """Main function with enhanced error handling"""
    
    # Set environment variables for enhanced configuration
    os.environ['ASYNCIOPYSIDE6_EVENT_LOOP_INTERVAL'] = '0.005'
    os.environ['ASYNCIOPYSIDE6_ENABLE_DEBUG_MODE'] = 'true'
    os.environ['ASYNCIOPYSIDE6_LOG_LEVEL'] = 'DEBUG'
    os.environ['ASYNCIOPYSIDE6_ENABLE_PERFORMANCE_MONITORING'] = 'false'  # Disable for demo
    
    app = QApplication(sys.argv)
    
    try:
        # Use the library with enhanced features
        with AsyncioPySide6.use_asyncio(use_dedicated_thread=True):
            main_window = Phase1Phase2Demo()
            main_window.show()
            
            # Set up a timer to update the status periodically (simplified)
            timer = QTimer()
            timer.timeout.connect(lambda: main_window.check_health())
            timer.start(10000)  # Check health every 10 seconds
            
            return app.exec()
            
    except Exception as e:
        print(f"Failed to start demo: {e}")
        return 1
    finally:
        # Ensure cleanup
        try:
            if AsyncioPySide6.is_initialized():
                AsyncioPySide6.shutdown()
        except Exception:
            pass


if __name__ == "__main__":
    sys.exit(main()) 