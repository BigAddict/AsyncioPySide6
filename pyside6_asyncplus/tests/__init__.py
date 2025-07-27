"""
Test suite for AsyncioPySide6 with QtAsyncio integration.

This package contains comprehensive tests for the refactored AsyncioPySide6
implementation that uses QtAsyncio as the base while adding advanced features.

Test Modules:
- test_core.py: Core functionality tests
- test_performance.py: Performance monitoring tests

Usage:
    python -m pytest AsyncioPySide6/tests/
    python -m pytest AsyncioPySide6/tests/test_core.py
    python -m pytest AsyncioPySide6/tests/test_performance.py
"""

# Test modules
__all__ = ["test_core", "test_performance"]
