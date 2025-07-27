AsyncioPySide6 Documentation
============================

Enhanced QtAsyncio integration with advanced async features for PySide6 applications.

.. image:: https://img.shields.io/badge/python-3.11+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python 3.11+

.. image:: https://img.shields.io/badge/PySide6-6.9.1+-green.svg
   :target: https://pypi.org/project/PySide6/
   :alt: PySide6

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: LICENSE
   :alt: License

Overview
--------

AsyncioPySide6 provides an enhanced wrapper around PySide6's built-in QtAsyncio that adds advanced features like timeout handling, retry logic, performance monitoring, and comprehensive error handling while maintaining full compatibility with QtAsyncio.

Key Features
^^^^^^^^^^^^

* **QtAsyncio Integration** - Built on top of PySide6's native async support
* **Advanced Task Management** - Timeout, retry, and progress tracking with thread-safe GUI updates
* **Performance Monitoring** - Real-time metrics and health checks with robust fallback mechanisms
* **Thread Safety** - Safe GUI operations and thread coordination with automatic thread marshaling
* **Comprehensive Error Handling** - Robust error management and recovery with graceful degradation
* **Configuration System** - Flexible configuration with environment variables
* **Backward Compatibility** - Maintains existing API compatibility
* **Comprehensive Testing** - Full test suite with 46 tests covering all functionality

Installation
------------

Prerequisites
^^^^^^^^^^^^^

* Python 3.11+
* PySide6 6.9.1+

Install from Source
^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/your-username/AsyncioPySide6.git
   cd AsyncioPySide6

   # Create virtual environment
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Install in development mode
   pip install -e .

Quick Start
-----------

Basic Usage
^^^^^^^^^^^

.. code-block:: python

   import asyncio
   from PySide6.QtWidgets import QApplication
   from AsyncioPySide6 import AsyncioPySide6

   # Create Qt application
   app = QApplication([])

   # Use AsyncioPySide6 with context manager
   with AsyncioPySide6():
       # Run async tasks
       async def my_task():
           await asyncio.sleep(2)
           print("Task completed!")
       
       # Run the task
       AsyncioPySide6.runTask(my_task())
       
       # Run the application
       app.exec()

Advanced Usage
^^^^^^^^^^^^^^

.. code-block:: python

   import asyncio
   from PySide6.QtWidgets import QApplication
   from AsyncioPySide6 import AsyncioPySide6

   app = QApplication([])

   with AsyncioPySide6():
       # Task with timeout
       async def timeout_task():
           await asyncio.sleep(5)  # Will timeout after 3 seconds
       
       AsyncioPySide6.runTaskWithTimeout(timeout_task(), timeout=3.0)
       
       # Task with retry logic
       async def retry_task():
           # Simulate flaky operation
           if random.random() < 0.7:
               raise Exception("Random failure")
           return "Success!"
       
       AsyncioPySide6.runTaskWithRetry(
           lambda: retry_task(),
           max_retries=3,
           retry_delay=1.0
       )
       
       # Task with thread-safe progress tracking
       def progress_callback(progress):
           print(f"Progress: {progress * 100:.0f}%")
       
       async def progress_task():
           for i in range(10):
               await asyncio.sleep(0.5)
               # Progress updates are automatically marshaled to GUI thread
       
       AsyncioPySide6.runTaskWithProgress(progress_task(), progress_callback)
       
       app.exec()

API Reference
-------------

Core Classes
^^^^^^^^^^^^

.. automodule:: AsyncioPySide6.nvd.AsyncioPySide6
   :members:
   :undoc-members:
   :show-inheritance:

Configuration
^^^^^^^^^^^^^

.. automodule:: AsyncioPySide6.nvd.config
   :members:
   :undoc-members:
   :show-inheritance:

Exceptions
^^^^^^^^^^

.. automodule:: AsyncioPySide6.nvd.exceptions
   :members:
   :undoc-members:
   :show-inheritance:

Performance Monitoring
^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: AsyncioPySide6.nvd.performance
   :members:
   :undoc-members:
   :show-inheritance:

Examples
--------

Basic Example
^^^^^^^^^^^^^

See :doc:`examples/basic_example` for a simple demonstration of:

* Basic async task execution
* Timeout handling
* Retry logic
* GUI thread safety

Advanced Example
^^^^^^^^^^^^^^^^

See :doc:`examples/advanced_example` for a comprehensive demonstration of:

* Performance monitoring with fallback mechanisms
* Real-time health checks with meaningful thresholds
* Thread-safe progress tracking with automatic GUI updates
* Complex async patterns
* Configuration management
* Memory and performance metrics display

Architecture
------------

QtAsyncio Integration
^^^^^^^^^^^^^^^^^^^^^

AsyncioPySide6 is built on top of PySide6's native QtAsyncio module, providing:

* **Native Integration** - Uses QtAsyncio's event loop management
* **Enhanced Features** - Adds advanced capabilities on top of QtAsyncio
* **Full Compatibility** - Maintains compatibility with QtAsyncio APIs
* **Performance** - Leverages QtAsyncio's optimized event loop
* **Thread Safety** - Automatic thread marshaling for GUI updates

Feature Comparison
^^^^^^^^^^^^^^^^^^

* **Basic async support**: QtAsyncio ✅ | AsyncioPySide6 ✅
* **Timeout handling**: QtAsyncio ❌ | AsyncioPySide6 ✅
* **Retry logic**: QtAsyncio ❌ | AsyncioPySide6 ✅
* **Progress tracking**: QtAsyncio ❌ | AsyncioPySide6 ✅ (Thread-safe)
* **Performance monitoring**: QtAsyncio ❌ | AsyncioPySide6 ✅ (With fallbacks)
* **Health checks**: QtAsyncio ❌ | AsyncioPySide6 ✅ (Robust)
* **Thread safety**: QtAsyncio ✅ | AsyncioPySide6 ✅ (Enhanced)
* **Configuration system**: QtAsyncio ❌ | AsyncioPySide6 ✅
* **Error handling**: QtAsyncio Basic | AsyncioPySide6 Advanced
* **Test coverage**: QtAsyncio ❌ | AsyncioPySide6 ✅ (46 tests)

Performance
-----------

AsyncioPySide6 is designed for high performance:

* **Minimal Overhead** - Direct QtAsyncio integration
* **Efficient Task Management** - Optimized task scheduling
* **Memory Management** - Proper resource cleanup
* **Monitoring** - Real-time performance tracking with fallback mechanisms
* **Thread Safety** - Automatic thread marshaling without performance impact

Error Handling
--------------

Comprehensive error handling with custom exceptions and graceful degradation:

* `AsyncioPySide6Error` - Base exception class
* `EventLoopError` - Event loop related errors
* `TaskTimeoutError` - Task timeout errors
* `TaskExecutionError` - Task execution errors
* `ConfigurationError` - Configuration errors
* **Graceful Degradation** - Fallback mechanisms when features aren't available
* **Robust Recovery** - Automatic error recovery and cleanup

Testing
-------

Comprehensive test suite with 46 tests covering all functionality:

* **Core Tests** (27 tests) - Basic functionality, task management, error handling
* **Performance Tests** (19 tests) - Monitoring, metrics, health checks
* **Thread Safety** - GUI thread marshaling and safety
* **Error Scenarios** - Timeout, retry, and failure handling
* **Integration Tests** - End-to-end functionality verification

Run tests with:

.. code-block:: bash

   python -m pytest tests/ -v

Contributing
------------

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

Development Setup
^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Install development dependencies
   pip install -r requirements-dev.txt

   # Run tests
   python -m pytest tests/

   # Run linting
   python -m flake8 AsyncioPySide6/

   # Generate documentation
   make docs

License
-------

This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
---------------

* PySide6 team for the excellent Qt bindings
* Python asyncio community for async/await patterns
* Qt team for QtAsyncio integration

Changelog
---------

Version 2.1.0
^^^^^^^^^^^^^

* **Thread-Safe Progress Tracking** - Automatic GUI thread marshaling for progress updates
* **Enhanced Performance Monitoring** - Robust fallback mechanisms and improved metrics
* **Improved Error Handling** - Graceful degradation and better error recovery
* **Comprehensive Test Suite** - 46 tests with full coverage and no warnings
* **Better Health Status** - Meaningful thresholds and fallback metrics
* **Memory Management** - Improved memory tracking and display
* **GUI Thread Safety** - All GUI updates properly marshaled to main thread

Version 2.0.0
^^^^^^^^^^^^^

* **Major Refactor** - Complete rewrite using QtAsyncio as base
* **Simplified Architecture** - Removed complex thread/timer implementations
* **Enhanced Features** - Advanced task management and monitoring
* **Better Documentation** - Comprehensive docstrings for Sphinx
* **Clean Examples** - Simplified example structure
* **Performance Improvements** - Direct QtAsyncio integration
* **Backward Compatibility** - Maintained existing API compatibility

Version 1.0.0
^^^^^^^^^^^^^

* Initial release with thread-based async implementation
* Basic task management features
* Configuration system
* Performance monitoring

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   examples/basic_example
   examples/advanced_example

