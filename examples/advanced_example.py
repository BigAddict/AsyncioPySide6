#!/usr/bin/env python3
"""
Advanced Example - AsyncioPySide6 with QtAsyncio Integration.

This example demonstrates advanced usage of AsyncioPySide6 with QtAsyncio integration.
It shows performance monitoring, health checks, progress tracking, and complex async patterns.
"""

import asyncio
import sys
import time
import random
from typing import List, Dict, Any
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
    QPushButton, QLabel, QTextEdit, QProgressBar, QGroupBox, QGridLayout
)
from PySide6.QtCore import QTimer, QThread, QObject

# Import our enhanced AsyncioPySide6
sys.path.append('..')
from AsyncioPySide6 import AsyncioPySide6, get_config, set_config, get_health_status


class AdvancedExample(QMainWindow):
    """
    Advanced example demonstrating AsyncioPySide6 with QtAsyncio integration.
    
    This example shows:
    - Performance monitoring and health checks
    - Progress tracking
    - Complex async patterns
    - Configuration management
    - Multiple concurrent tasks
    - Error handling and recovery
    """
    
    def __init__(self):
        """Initialize the advanced example window."""
        super().__init__()
        self.setWindowTitle("AsyncioPySide6 Advanced Example")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create UI sections
        self._create_status_section(main_layout)
        self._create_controls_section(main_layout)
        self._create_progress_section(main_layout)
        self._create_log_section(main_layout)
        
        # Initialize timers and counters
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(1000)  # Update every second
        self.timer_count = 0
        
        # Task tracking
        self.active_tasks = 0
        self.completed_tasks = 0
        self.failed_tasks = 0
        
        # Initialize AsyncioPySide6 with performance monitoring
        self._setup_asyncio()
    
    def _create_status_section(self, parent_layout):
        """Create the status section with health information.
        
        Args:
            parent_layout: The parent layout to add widgets to
        """
        status_group = QGroupBox("System Status")
        status_layout = QGridLayout(status_group)
        
        # Health status labels
        self.health_status_label = QLabel("Health: Unknown")
        status_layout.addWidget(QLabel("System Health:"), 0, 0)
        status_layout.addWidget(self.health_status_label, 0, 1)
        
        self.task_count_label = QLabel("Tasks: 0")
        status_layout.addWidget(QLabel("Active Tasks:"), 1, 0)
        status_layout.addWidget(self.task_count_label, 1, 1)
        
        self.memory_label = QLabel("Memory: Unknown")
        status_layout.addWidget(QLabel("Memory Usage:"), 2, 0)
        status_layout.addWidget(self.memory_label, 2, 1)
        
        self.performance_label = QLabel("Performance: Unknown")
        status_layout.addWidget(QLabel("Performance:"), 3, 0)
        status_layout.addWidget(self.performance_label, 3, 1)
        
        parent_layout.addWidget(status_group)
    
    def _create_controls_section(self, parent_layout):
        """Create the controls section with action buttons.
        
        Args:
            parent_layout: The parent layout to add widgets to
        """
        controls_group = QGroupBox("Controls")
        controls_layout = QHBoxLayout(controls_group)
        
        # Basic task button
        self.basic_btn = QPushButton("Basic Task")
        self.basic_btn.clicked.connect(self.run_basic_task)
        controls_layout.addWidget(self.basic_btn)
        
        # Progress task button
        self.progress_btn = QPushButton("Progress Task")
        self.progress_btn.clicked.connect(self.run_progress_task)
        controls_layout.addWidget(self.progress_btn)
        
        # Concurrent tasks button
        self.concurrent_btn = QPushButton("Concurrent Tasks")
        self.concurrent_btn.clicked.connect(self.run_concurrent_tasks)
        controls_layout.addWidget(self.concurrent_btn)
        
        # Stress test button
        self.stress_btn = QPushButton("Stress Test")
        self.stress_btn.clicked.connect(self.run_stress_test)
        controls_layout.addWidget(self.stress_btn)
        
        # Configuration button
        self.config_btn = QPushButton("Show Config")
        self.config_btn.clicked.connect(self.show_configuration)
        controls_layout.addWidget(self.config_btn)
        
        parent_layout.addWidget(controls_group)
    
    def _create_progress_section(self, parent_layout):
        """Create the progress section with progress bars.
        
        Args:
            parent_layout: The parent layout to add widgets to
        """
        progress_group = QGroupBox("Progress Tracking")
        progress_layout = QVBoxLayout(progress_group)
        
        # Progress bar for current task
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)
        
        # Progress label
        self.progress_label = QLabel("No active progress")
        progress_layout.addWidget(self.progress_label)
        
        parent_layout.addWidget(progress_group)
    
    def _create_log_section(self, parent_layout):
        """Create the log section with text display.
        
        Args:
            parent_layout: The parent layout to add widgets to
        """
        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        log_layout.addWidget(self.log_text)
        
        parent_layout.addWidget(log_group)
    
    def _setup_asyncio(self):
        """Setup AsyncioPySide6 with performance monitoring."""
        # Enable performance monitoring
        config = get_config()
        config.enable_performance_monitoring = True
        config.enable_debug_mode = True
        config.enable_metrics_collection = True
        config.enable_memory_monitoring = True
        config.enable_task_monitoring = True
        set_config(config)
        
        # Start performance monitoring (handle event loop issues gracefully)
        try:
            from AsyncioPySide6.nvd.performance import start_performance_monitoring
            start_performance_monitoring()
            self.log("AsyncioPySide6 initialized with performance monitoring")
        except Exception as e:
            self.log(f"Performance monitoring initialization failed: {e}")
            self.log("Continuing without performance monitoring...")
    
    def log(self, message: str):
        """Add message to log with timestamp.
        
        Args:
            message: The message to log
        """
        self.log_text.append(f"[{self.timer_count}s] {message}")
    
    def update_metrics(self):
        """Update performance metrics manually."""
        try:
            from AsyncioPySide6.nvd.performance import get_performance_monitor
            monitor = get_performance_monitor()

            # Check if the monitor has the _has_event_loop method
            if hasattr(monitor, '_has_event_loop'):
                # Create a new metric if we have an event loop
                if monitor._has_event_loop():
                    metrics = monitor._collect_metrics()
                    monitor.metrics_history.append(metrics)
            else:
                # Fallback: try to create a basic metric
                try:
                    import psutil
                    process = psutil.Process()
                    memory_info = process.memory_info()
                    memory_usage_mb = memory_info.rss / 1024 / 1024
                    memory_percentage = (memory_info.rss / psutil.virtual_memory().total) * 100
                    
                    from AsyncioPySide6.nvd.performance import PerformanceMetrics
                    initial_metric = PerformanceMetrics(
                        timestamp=time.time(),
                        active_tasks=self.active_tasks,
                        memory_usage_mb=memory_usage_mb,
                        memory_percentage=memory_percentage,
                        event_loop_latency_ms=0.0,
                        task_completion_rate=0.0,
                        error_rate=0.0,
                        cpu_usage_percentage=process.cpu_percent()
                    )
                    monitor.metrics_history.append(initial_metric)
                except Exception as e:
                    self.log(f"Could not create fallback metric: {e}")
        except Exception as e:
            self.log(f"Error updating metrics: {e}")

    def update_status(self):
        """Update status information."""
        self.timer_count += 1
        
        # Update metrics periodically
        if self.timer_count % 5 == 0:  # Update every 5 seconds
            self.update_metrics()
        
        # Update task counts
        self.task_count_label.setText(f"Tasks: {self.active_tasks}")
        
        # Get health status
        try:
            health = get_health_status()
            status = health.get('status', 'Unknown')
            self.health_status_label.setText(f"Health: {status}")
            
            # Get memory and performance from metrics if available
            metrics = health.get('metrics', {})
            memory_percent = metrics.get('memory_percentage', 0)
            memory_mb = metrics.get('memory_usage_mb', 0)
            
            # If no metrics available, try to get basic memory info
            if memory_percent == 0 and memory_mb == 0:
                try:
                    import psutil
                    process = psutil.Process()
                    memory_info = process.memory_info()
                    memory_mb = memory_info.rss / 1024 / 1024
                    memory_percent = (memory_info.rss / psutil.virtual_memory().total) * 100
                    self.memory_label.setText(f"Memory: {memory_percent:.1f}% ({memory_mb:.1f}MB)")
                except Exception:
                    self.memory_label.setText("Memory: Unknown")
            else:
                self.memory_label.setText(f"Memory: {memory_percent:.1f}% ({memory_mb:.1f}MB)")
            
            # Calculate performance score
            if metrics:
                completion_rate = metrics.get('task_completion_rate', 0)
                error_rate = metrics.get('error_rate', 0)
                # Calculate performance as a combination of completion rate and low error rate
                if completion_rate > 0:
                    performance_score = (completion_rate * 100) - (error_rate * 100)
                else:
                    # If no completion rate, base it on error rate and active tasks
                    performance_score = max(0, 100 - (error_rate * 100))
                self.performance_label.setText(f"Performance: {performance_score:.1f}%")
            else:
                # Fallback performance calculation based on task completion
                if self.completed_tasks > 0 or self.failed_tasks > 0:
                    total_tasks = self.completed_tasks + self.failed_tasks
                    if total_tasks > 0:
                        completion_rate = self.completed_tasks / total_tasks
                        performance_score = completion_rate * 100
                        self.performance_label.setText(f"Performance: {performance_score:.1f}%")
                    else:
                        self.performance_label.setText("Performance: 0.0%")
                else:
                    # If no tasks have been run, show a default value
                    self.performance_label.setText("Performance: 100.0%")
                
        except Exception as e:
            self.log(f"Error getting health status: {e}")
            self.health_status_label.setText("Health: Error")
            self.memory_label.setText("Memory: Error")
            self.performance_label.setText("Performance: Error")
    
    async def basic_async_task(self):
        """Basic async task with logging.
        
        Returns:
            str: Result message
        """
        self.log("Starting basic async task...")
        await asyncio.sleep(2)
        self.log("Basic async task completed!")
        return "Basic task completed"
    
    async def progress_async_task(self, progress_callback):
        """Async task with progress reporting.
        
        Args:
            progress_callback: Callback function for progress updates
            
        Returns:
            str: Result message
        """
        self.log("Starting progress async task...")
        
        try:
            for i in range(10):
                await asyncio.sleep(0.5)
                progress = (i + 1) / 10.0
                progress_callback(progress)
                self.log(f"Progress: {progress * 100:.0f}%")
            
            self.log("Progress async task completed!")
            return "Progress task completed"
        except Exception as e:
            self.log(f"Progress task failed: {e}")
            raise
    
    async def concurrent_task(self, task_id: int):
        """Concurrent task that simulates work.
        
        Args:
            task_id: Unique identifier for this task
            
        Returns:
            str: Result message
        """
        self.log(f"Starting concurrent task {task_id}...")
        
        # Simulate variable work time
        work_time = random.uniform(1, 3)
        await asyncio.sleep(work_time)
        
        self.log(f"Concurrent task {task_id} completed!")
        return f"Concurrent task {task_id} completed"
    
    async def stress_task(self, task_id: int):
        """Stress test task that might fail.
        
        Args:
            task_id: Unique identifier for this task
            
        Returns:
            str: Result message
        """
        self.log(f"Starting stress task {task_id}...")
        
        # Simulate potential failure
        if random.random() < 0.1:  # 10% chance of failure
            raise Exception(f"Stress task {task_id} failed randomly")
        
        # Simulate CPU-intensive work
        work_time = random.uniform(0.5, 2.0)
        await asyncio.sleep(work_time)
        
        self.log(f"Stress task {task_id} completed!")
        return f"Stress task {task_id} completed"
    
    def run_basic_task(self):
        """Run a basic async task."""
        self.log("=== Running Basic Task ===")
        self.active_tasks += 1
        
        def on_complete():
            """Handle task completion."""
            self.active_tasks -= 1
            self.completed_tasks += 1
            self.log("Basic task completed in GUI thread")
        
        AsyncioPySide6.runTask(self.basic_async_task())
        QTimer.singleShot(2500, on_complete)  # Schedule completion callback
    
    def run_progress_task(self):
        """Run a task with progress tracking."""
        self.log("=== Running Progress Task ===")
        self.active_tasks += 1
        
        # Show progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_label.setText("Progress task running...")
        
        def progress_callback(progress: float):
            """Update progress bar in GUI thread.
            
            Args:
                progress: Progress value between 0.0 and 1.0
            """
            # Ensure progress is within bounds
            progress = max(0.0, min(1.0, progress))
            # Use QTimer to ensure GUI thread execution
            QTimer.singleShot(0, lambda: self.progress_bar.setValue(int(progress * 100)))
        
        def on_complete():
            """Handle task completion."""
            self.active_tasks -= 1
            self.completed_tasks += 1
            self.progress_bar.setVisible(False)
            self.progress_label.setText("Progress task completed!")
            self.log("Progress task completed in GUI thread")
        
        AsyncioPySide6.runTaskWithProgress(
            self.progress_async_task(progress_callback),
            progress_callback
        )
        QTimer.singleShot(6000, on_complete)  # Schedule completion callback
    
    def run_concurrent_tasks(self):
        """Run multiple concurrent tasks."""
        self.log("=== Running Concurrent Tasks ===")
        num_tasks = 5
        self.active_tasks += num_tasks
        
        def on_complete():
            """Handle task completion."""
            self.active_tasks -= num_tasks
            self.completed_tasks += num_tasks
            self.log("All concurrent tasks completed in GUI thread")
        
        # Run multiple concurrent tasks
        for i in range(num_tasks):
            AsyncioPySide6.runTask(self.concurrent_task(i + 1))
        
        # Schedule completion callback
        QTimer.singleShot(4000, on_complete)  # Schedule completion callback
    
    def run_stress_test(self):
        """Run stress test with multiple tasks and retry logic."""
        self.log("=== Running Stress Test ===")
        num_tasks = 10
        self.active_tasks += num_tasks
        
        def on_complete():
            """Handle task completion."""
            self.active_tasks -= num_tasks
            self.completed_tasks += num_tasks
            self.log("Stress test completed in GUI thread")
        
        # Run stress test tasks with retry logic
        for i in range(num_tasks):
            AsyncioPySide6.runTaskWithRetry(
                lambda: self.stress_task(i + 1),
                max_retries=2,
                retry_delay=0.5
            )
        
        # Schedule completion callback
        QTimer.singleShot(5000, on_complete)  # Schedule completion callback
    
    def show_configuration(self):
        """Show current configuration."""
        self.log("=== Current Configuration ===")
        
        config = get_config()
        self.log(f"Task timeout: {config.task_timeout}s")
        self.log(f"Max retries: {config.max_retries}")
        self.log(f"Retry delay: {config.retry_delay}s")
        self.log(f"Performance monitoring: {config.enable_performance_monitoring}")
        self.log(f"Debug mode: {config.enable_debug_mode}")
        
        # Show health status
        health = get_health_status()
        self.log(f"Health status: {health}")


def main():
    """Main function to run the advanced example."""
    app = QApplication(sys.argv)
    
    # Create and show the example window
    example = AdvancedExample()
    example.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 