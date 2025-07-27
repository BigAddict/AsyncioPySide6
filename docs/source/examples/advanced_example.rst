Advanced Example
================

This example demonstrates advanced features of AsyncioPySide6 including performance monitoring, real-time health checks, thread-safe progress tracking, complex async patterns, and configuration management.

Overview
--------

The advanced example showcases:

* Performance monitoring with fallback mechanisms
* Real-time health checks with meaningful thresholds
* Thread-safe progress tracking with automatic GUI updates
* Complex async patterns and task coordination
* Configuration management and environment variables
* Memory and performance metrics display
* Advanced error handling and recovery

Code Example
------------

.. literalinclude:: ../../../examples/advanced_example.py
   :language: python
   :caption: Advanced Example (examples/advanced_example.py)

Key Features Demonstrated
-------------------------

Performance Monitoring
^^^^^^^^^^^^^^^^^^^^^^

Demonstrates comprehensive performance tracking with fallback mechanisms:

.. code-block:: python

   # Monitor performance metrics
   health_status = AsyncioPySide6.get_health_status()
   print(f"Health Status: {health_status}")
   
   # Get task count
   task_count = AsyncioPySide6.get_task_count()
   print(f"Active Tasks: {task_count}")

Real-Time Health Checks
^^^^^^^^^^^^^^^^^^^^^^^

Shows how to implement meaningful health monitoring:

.. code-block:: python

   def check_system_health():
       health = AsyncioPySide6.get_health_status()
       
       # Check memory usage
       if health.get('memory_usage_percent', 0) > 80:
           print("Warning: High memory usage!")
       
       # Check task count
       if health.get('active_tasks', 0) > 10:
           print("Warning: High task count!")
       
       # Check performance metrics
       if health.get('avg_task_duration', 0) > 5.0:
           print("Warning: Slow task execution!")

Thread-Safe Progress Tracking
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Demonstrates automatic GUI thread marshaling for progress updates:

.. code-block:: python

   def progress_callback(progress):
       # This callback is automatically marshaled to the GUI thread
       progress_bar.setValue(int(progress * 100))
       status_label.setText(f"Progress: {progress * 100:.0f}%")

   async def complex_task_with_progress():
       for i in range(10):
           await asyncio.sleep(0.5)
           # Progress updates are automatically thread-safe
           yield (i + 1) / 10

   AsyncioPySide6.runTaskWithProgress(
       complex_task_with_progress(), 
       progress_callback
   )

Configuration Management
^^^^^^^^^^^^^^^^^^^^^^^^

Shows how to use the configuration system:

.. code-block:: python

   from AsyncioPySide6.nvd.config import get_config, set_config

   # Get current configuration
   config = get_config()
   print(f"Current timeout: {config.task_timeout}")
   
   # Modify configuration
   config.task_timeout = 30.0
   config.max_retries = 5
   set_config(config)

Complex Async Patterns
^^^^^^^^^^^^^^^^^^^^^^

Demonstrates advanced async task coordination:

.. code-block:: python

   async def coordinated_tasks():
       # Run multiple tasks concurrently
       tasks = [
           task1(),
           task2(),
           task3()
       ]
       
       # Wait for all tasks to complete
       results = await asyncio.gather(*tasks, return_exceptions=True)
       
       # Process results
       for i, result in enumerate(results):
           if isinstance(result, Exception):
               print(f"Task {i} failed: {result}")
           else:
               print(f"Task {i} succeeded: {result}")

Memory and Performance Metrics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Shows how to display comprehensive system metrics:

.. code-block:: python

   def display_metrics():
       health = AsyncioPySide6.get_health_status()
       
       metrics_text = f"""
       System Metrics:
       - Memory Usage: {health.get('memory_usage_percent', 0):.1f}%
       - Active Tasks: {health.get('active_tasks', 0)}
       - Avg Task Duration: {health.get('avg_task_duration', 0):.2f}s
       - Total Tasks: {health.get('total_tasks', 0)}
       - Success Rate: {health.get('success_rate', 0):.1f}%
       """
       
       metrics_label.setText(metrics_text)

Advanced Error Handling
^^^^^^^^^^^^^^^^^^^^^^^

Demonstrates robust error recovery and graceful degradation:

.. code-block:: python

   async def robust_task():
       try:
           # Attempt the operation
           result = await risky_operation()
           return result
       except Exception as e:
           # Log the error
           print(f"Task failed: {e}")
           
           # Try fallback operation
           try:
               return await fallback_operation()
           except Exception as fallback_error:
               print(f"Fallback also failed: {fallback_error}")
               raise

Running the Example
-------------------

To run the advanced example:

.. code-block:: bash

   cd examples
   python advanced_example.py

Expected Output
---------------

The advanced example will demonstrate:

* Real-time performance monitoring with metrics display
* Health status monitoring with meaningful thresholds
* Thread-safe progress bars and status updates
* Configuration management and environment variable usage
* Complex async task coordination
* Memory and performance metrics in the GUI
* Advanced error handling with fallback mechanisms
* Comprehensive logging and debugging information

This example showcases the full power of AsyncioPySide6 for building robust, high-performance Qt applications with advanced async capabilities. 