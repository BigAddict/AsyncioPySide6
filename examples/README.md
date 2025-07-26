# AsyncioPySide6 Examples

This directory contains examples demonstrating the usage of AsyncioPySide6 with QtAsyncio integration.

## Examples Overview

### Basic Example (`basic_example.py`)

A simple example that demonstrates the core features of AsyncioPySide6:

- **Basic async task execution** - Simple async tasks with QtAsyncio integration
- **Timeout handling** - Tasks that timeout and proper error handling
- **Retry logic** - Tasks that fail and are retried automatically
- **GUI thread safety** - Safe GUI updates from async tasks

**Key Features Demonstrated:**
- `AsyncioPySide6.runTask()` - Basic task execution
- `AsyncioPySide6.runTaskWithTimeout()` - Timeout handling
- `AsyncioPySide6.runTaskWithRetry()` - Retry logic
- `AsyncioPySide6.invokeInGuiThread()` - GUI thread safety

### Advanced Example (`advanced_example.py`)

A comprehensive example that demonstrates all advanced features:

- **Performance monitoring** - Real-time performance tracking
- **Health checks** - System health monitoring
- **Progress tracking** - Real-time progress updates
- **Complex async patterns** - Multiple concurrent tasks
- **Configuration management** - Dynamic configuration
- **Error handling and recovery** - Robust error handling

**Key Features Demonstrated:**
- Performance monitoring and health checks
- Progress tracking with callbacks
- Multiple concurrent task execution
- Stress testing with retry logic
- Configuration management
- Real-time status updates

## Running the Examples

### Prerequisites

1. Install PySide6:
   ```bash
   pip install PySide6
   ```

2. Ensure you have the AsyncioPySide6 library installed or in your Python path.

### Running Basic Example

```bash
cd examples
python basic_example.py
```

This will open a simple GUI application with buttons to test:
- Basic async tasks
- Tasks with timeout handling
- Tasks with retry logic

### Running Advanced Example

```bash
cd examples
python advanced_example.py
```

This will open a comprehensive GUI application with:
- Real-time system status monitoring
- Performance tracking
- Progress bars
- Multiple task types
- Configuration display

## Example Features

### Basic Example Features

1. **Simple Task Execution**
   - Demonstrates basic async task scheduling
   - Shows integration with QtAsyncio
   - Includes proper error handling

2. **Timeout Handling**
   - Shows how to set timeouts for tasks
   - Demonstrates timeout error handling
   - Includes user feedback

3. **Retry Logic**
   - Demonstrates automatic retry on failure
   - Shows configurable retry parameters
   - Includes failure simulation

4. **GUI Thread Safety**
   - Shows safe GUI updates from async tasks
   - Demonstrates proper thread handling
   - Includes real-time status updates

### Advanced Example Features

1. **Performance Monitoring**
   - Real-time performance metrics
   - Memory usage tracking
   - Task completion rates

2. **Health Checks**
   - System health monitoring
   - Error rate tracking
   - Performance scoring

3. **Progress Tracking**
   - Real-time progress updates
   - Progress bar integration
   - Callback-based progress reporting

4. **Concurrent Tasks**
   - Multiple simultaneous tasks
   - Task coordination
   - Resource management

5. **Stress Testing**
   - High-load task execution
   - Error simulation
   - Recovery mechanisms

6. **Configuration Management**
   - Dynamic configuration display
   - Runtime configuration changes
   - Performance tuning

## Code Structure

Both examples follow a clean, well-documented structure:

- **Class-based design** - Organized, maintainable code
- **Comprehensive docstrings** - Sphinx-ready documentation
- **Type hints** - Better IDE support and code clarity
- **Error handling** - Robust error management
- **GUI integration** - Clean Qt integration

## Learning Path

1. **Start with Basic Example** - Understand core concepts
2. **Study the code** - Review implementation details
3. **Run Advanced Example** - See full feature set
4. **Modify examples** - Experiment with different patterns
5. **Apply to your projects** - Use patterns in your applications

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure PySide6 is installed
   - Check Python path includes parent directory

2. **Runtime Errors**
   - Verify QtAsyncio is available in your PySide6 installation
   - Check for conflicting event loops

3. **Performance Issues**
   - Monitor system resources
   - Adjust configuration parameters
   - Check for memory leaks

### Getting Help

- Review the main library documentation
- Check the configuration options
- Examine the performance monitoring output
- Look at the health status information

## Contributing

When adding new examples:

1. **Follow the existing structure** - Use the same patterns
2. **Add comprehensive docstrings** - Document all functions
3. **Include type hints** - For better code clarity
4. **Test thoroughly** - Ensure examples work correctly
5. **Update this README** - Document new examples

## License

These examples are part of the AsyncioPySide6 project and follow the same license terms. 