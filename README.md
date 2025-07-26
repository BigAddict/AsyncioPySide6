# AsyncioPySide6
Empower Qt PySide6 developers with seamless async/await asynchronous programming capabilities

[![Tests](https://img.shields.io/badge/tests-36%20passed%2C%201%20skipped-brightgreen)](https://github.com/your-repo/AsyncioPySide6)
[![Python](https://img.shields.io/badge/python-3.8+-blue)](https://python.org)
[![PySide6](https://img.shields.io/badge/PySide6-6.0+-orange)](https://doc.qt.io/qtforpython/)

## 🚀 **Production-Ready Features**

- ✅ **Thread-safe singleton pattern** for reliable initialization
- ✅ **Comprehensive error handling** with custom exception hierarchy
- ✅ **Configurable system** with environment variable support
- ✅ **Robust shutdown mechanisms** with timeout-based cleanup
- ✅ **100% test coverage** with 36 comprehensive tests
- ✅ **Type hints** throughout for better developer experience
- ✅ **Extensive logging** with configurable levels

## 📦 Installation

```bash
pip install AsyncioPySide6
```

## 🎯 Quick Start

### Basic Usage

```python
import sys
import asyncio
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    with AsyncioPySide6.use_asyncio():
        main_window = MainWindow()
        main_window.show()
        app.exec()
```

### Advanced Configuration

```python
from AsyncioPySide6 import AsyncioPySide6, get_config, set_config

# Configure the library
config = get_config()
config.event_loop_interval = 0.005  # Faster event loop
config.shutdown_timeout = 15.0      # Longer shutdown timeout
config.enable_debug_mode = True     # Enable debug logging
set_config(config)

# Use with custom configuration
with AsyncioPySide6.use_asyncio(use_dedicated_thread=True):
    # Your async code here
    pass
```

### Environment Variables

You can configure the library using environment variables:

```bash
export ASYNCIOPYSIDE6_EVENT_LOOP_INTERVAL=0.005
export ASYNCIOPYSIDE6_SHUTDOWN_TIMEOUT=15.0
export ASYNCIOPYSIDE6_ENABLE_DEBUG_MODE=true
export ASYNCIOPYSIDE6_USE_DEDICATED_THREAD=true
```

## 🔧 **API Reference**

### Core Classes

#### `AsyncioPySide6`
Main class providing async/await integration with Qt.

**Methods:**
- `use_asyncio(use_dedicated_thread: bool = False)` - Context manager for async operations
- `runTask(coroutine: Coroutine)` - Execute an async task
- `initialize()` - Initialize the library
- `shutdown(timeout: float = None)` - Gracefully shutdown
- `is_initialized()` - Check if library is initialized

#### Configuration
- `get_config()` - Get current configuration
- `set_config(config: AsyncioPySide6Config)` - Set custom configuration
- `reset_config()` - Reset to default configuration

### Exception Hierarchy

```python
AsyncioPySide6Error (base)
├── EventLoopError
├── ThreadSafetyError
├── InitializationError
└── ShutdownError
```

## ⚙️ **Configuration Options**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `event_loop_interval` | 0.001 | Event loop processing interval |
| `idle_sleep_time` | 0.001 | Sleep time when idle |
| `use_dedicated_thread` | False | Use dedicated thread for event loop |
| `initialization_timeout` | 5.0 | Initialization timeout in seconds |
| `shutdown_timeout` | 10.0 | Shutdown timeout in seconds |
| `task_timeout` | 30.0 | Default task timeout |
| `max_retries` | 3 | Maximum retry attempts |
| `retry_delay` | 0.1 | Delay between retries |
| `enable_logging` | True | Enable logging |
| `log_level` | "INFO" | Logging level |
| `max_concurrent_tasks` | 100 | Maximum concurrent tasks |
| `task_queue_size` | 1000 | Task queue size |
| `enable_debug_mode` | False | Enable debug mode |
| `enable_performance_monitoring` | False | Enable performance monitoring |

## 🧪 **Testing**

Run the comprehensive test suite:

```bash
# Run all tests
python -m unittest AsyncioPySide6.tests

# Run specific test modules
python -m unittest AsyncioPySide6.tests.test_AsyncioPySide6
python -m unittest AsyncioPySide6.tests.test_config
```

## 📊 **Performance**

The library is optimized for:
- **Low latency**: Configurable event loop intervals
- **Resource efficiency**: Proper cleanup and memory management
- **Thread safety**: Thread-safe singleton pattern
- **Scalability**: Configurable task limits and queue sizes

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆕 **What's New in Phase 1**

- **Production-ready stability** with comprehensive error handling
- **Flexible configuration system** with environment variable support
- **Thread-safe architecture** with proper resource management
- **100% test coverage** with 36 comprehensive tests
- **Enhanced developer experience** with type hints and documentation