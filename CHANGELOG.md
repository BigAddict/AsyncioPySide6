# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-07-27

### Added
- **Initial Release** - Fork of AsyncioPySide6 with enhanced features
- **Thread-Safe Progress Tracking** - Automatic GUI thread marshaling for progress updates
- **Enhanced Performance Monitoring** - Robust fallback mechanisms and improved metrics
- **Improved Error Handling** - Graceful degradation and better error recovery
- **Comprehensive Test Suite** - 46 tests with full coverage and no warnings
- **Better Health Status** - Meaningful thresholds and fallback metrics
- **Memory Management** - Improved memory tracking and display
- **GUI Thread Safety** - All GUI updates properly marshaled to main thread
- **PyPI Ready** - Complete package structure for PyPI distribution
- **New Package Name** - Renamed to `pyside6-asyncplus` for clarity
- **Simplified API** - New `app` module with cleaner interface
- **BSD-3-Clause License** - Proper license attribution to original author
- **Documentation Updates** - Comprehensive README with installation instructions
- **Example Updates** - Updated examples to use new package structure

### Changed
- **Package Structure** - Reorganized from `AsyncioPySide6` to `pyside6_asyncplus`
- **Import Interface** - New `from pyside6_asyncplus.app import run` pattern
- **Version Numbering** - Reset to 0.1.0 for new package identity
- **License Attribution** - Added proper attribution to original author @nguyenvuduc
- **Configuration** - Updated environment variable prefixes to `PYSIDE6_ASYNCPLUS_`

### Technical Details
- **Base Implementation** - Built on PySide6's native QtAsyncio
- **Advanced Features** - Timeout, retry, progress tracking, performance monitoring
- **Thread Safety** - Automatic thread marshaling for GUI operations
- **Error Recovery** - Graceful degradation when features aren't available
- **Performance** - Minimal overhead with direct QtAsyncio integration
- **Testing** - 46 comprehensive tests covering all functionality
- **Documentation** - Full API reference and usage examples

### Acknowledgments
- Original author @nguyenvuduc for the base AsyncioPySide6 implementation
- PySide6 team for excellent Qt bindings
- Python asyncio community for async/await patterns
- Qt team for QtAsyncio integration

---

## Original AsyncioPySide6 Changelog

### Version 2.1.0
- Thread-Safe Progress Tracking
- Enhanced Performance Monitoring
- Improved Error Handling
- Comprehensive Test Suite
- Better Health Status
- Memory Management
- GUI Thread Safety

### Version 2.0.0
- Major Refactor using QtAsyncio as base
- Simplified Architecture
- Enhanced Features
- Better Documentation
- Clean Examples
- Performance Improvements
- Backward Compatibility

### Version 1.0.0
- Initial release with thread-based async implementation
- Basic task management features
- Configuration system
- Performance monitoring 