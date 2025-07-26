# AsyncioPySide6 Examples

This directory contains example applications demonstrating the usage of the AsyncioPySide6 library.

## Examples

### 1. Basic Usage (`basic_usage.py`)
A simple example showing basic asyncio integration with PySide6.

**Features demonstrated:**
- Basic GUI setup with QMainWindow
- Simple asynchronous task execution
- Context manager usage
- Error handling

**To run:**
```bash
# Activate virtual environment and set PYTHONPATH
source .venv/bin/activate
PYTHONPATH=.venv/lib/python3.11/site-packages python examples/basic_usage.py
```

### 2. Advanced Usage (`advanced_usage.py`)
A comprehensive example showcasing the new Phase 1 features.

**Features demonstrated:**
- Configuration system with environment variables
- Advanced error handling with custom exceptions
- Multiple concurrent tasks
- Performance monitoring
- Debug logging
- Configuration changes at runtime

**To run:**
```bash
# Activate virtual environment and set PYTHONPATH
source .venv/bin/activate
PYTHONPATH=.venv/lib/python3.11/site-packages python examples/advanced_usage.py
```

## Requirements

- Python 3.11+
- PySide6 6.9.1+
- AsyncioPySide6 library (installed in virtual environment)

## Notes

- Both examples use the virtual environment to ensure proper dependency isolation
- The PYTHONPATH is set to include the virtual environment's site-packages directory
- The examples demonstrate proper error handling and resource cleanup
- The GUI windows will show real-time updates as the asynchronous tasks execute

## Troubleshooting

If you encounter import errors:
1. Ensure the virtual environment is activated: `source .venv/bin/activate`
2. Verify PySide6 is installed: `pip list | grep PySide6`
3. Set the PYTHONPATH correctly: `PYTHONPATH=.venv/lib/python3.11/site-packages`

If you encounter memory issues:
- The examples have been updated to use `QWidget` instead of `QMainWindow` as central widgets to avoid memory corruption
- All event loop interactions are properly handled with try-catch blocks 