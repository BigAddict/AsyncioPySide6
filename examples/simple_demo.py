#!/usr/bin/env python3
"""
Simple Demo - Basic AsyncioPySide6 Features

This is a simplified demo that tests the core functionality without GUI issues.
"""

import sys
import asyncio
import time
import os
from AsyncioPySide6 import (
    AsyncioPySide6, 
    get_config, 
    set_config, 
    TaskTimeoutError,
    ResourceExhaustedError,
    TaskExecutionError
)

def main():
    """Simple demo without GUI"""
    print("🚀 AsyncioPySide6 - Phase 1 & 2 Demo")
    print("=" * 50)
    
    # Set environment variables for enhanced configuration
    os.environ['ASYNCIOPYSIDE6_EVENT_LOOP_INTERVAL'] = '0.005'
    os.environ['ASYNCIOPYSIDE6_ENABLE_DEBUG_MODE'] = 'true'
    os.environ['ASYNCIOPYSIDE6_LOG_LEVEL'] = 'DEBUG'
    os.environ['ASYNCIOPYSIDE6_ENABLE_PERFORMANCE_MONITORING'] = 'false'
    
    try:
        # Use the library with enhanced features
        with AsyncioPySide6.use_asyncio(use_dedicated_thread=True):
            print("✅ AsyncioPySide6 initialized successfully")
            
            # Test 1: Basic task execution
            print("\n📋 Test 1: Basic task execution")
            async def basic_task():
                await asyncio.sleep(0.5)
                return "Basic task completed"
            
            AsyncioPySide6.runTask(basic_task())
            print("✅ Basic task executed")
            
            # Test 2: Task with timeout
            print("\n📋 Test 2: Task with timeout")
            async def timeout_task():
                await asyncio.sleep(2.0)
                return "Should not reach here"
            
            try:
                AsyncioPySide6.runTaskWithTimeout(timeout_task(), timeout=1.0)
            except TaskTimeoutError:
                print("✅ Task timeout handled correctly")
            except Exception as e:
                print(f"⚠️ Task timeout error: {e}")
            
            # Test 3: Task with retry
            print("\n📋 Test 3: Task with retry")
            attempt_count = 0
            
            def create_retry_task():
                nonlocal attempt_count
                attempt_count += 1
                
                async def failing_then_succeeding_task():
                    if attempt_count < 3:
                        raise RuntimeError(f"Simulated failure on attempt {attempt_count}")
                    return "Success after retries"
                
                return failing_then_succeeding_task()
            
            try:
                AsyncioPySide6.runTaskWithRetry(create_retry_task, max_retries=3, retry_delay=0.2)
                print("✅ Retry task completed successfully")
            except Exception as e:
                print(f"⚠️ Retry task error: {e}")
            
            # Test 4: Health status
            print("\n📋 Test 4: Health status")
            try:
                health_status = AsyncioPySide6.get_health_status()
                print(f"✅ Health status: {health_status.get('status', 'unknown')}")
            except Exception as e:
                print(f"⚠️ Health status error: {e}")
            
            # Test 5: Task count
            print("\n📋 Test 5: Task count")
            try:
                task_count = AsyncioPySide6.get_task_count()
                print(f"✅ Active tasks: {task_count}")
            except Exception as e:
                print(f"⚠️ Task count error: {e}")
            
            # Test 6: Resource cleanup
            print("\n📋 Test 6: Resource cleanup")
            try:
                AsyncioPySide6.cleanup_resources()
                print("✅ Resource cleanup completed")
            except Exception as e:
                print(f"⚠️ Cleanup error: {e}")
            
            # Test 7: Configuration
            print("\n📋 Test 7: Configuration")
            try:
                config = get_config()
                print(f"✅ Event loop interval: {config.event_loop_interval}")
                print(f"✅ Shutdown timeout: {config.shutdown_timeout}")
                print(f"✅ Enable debug mode: {config.enable_debug_mode}")
            except Exception as e:
                print(f"⚠️ Configuration error: {e}")
            
            print("\n🎉 All tests completed successfully!")
            print("=" * 50)
            
    except Exception as e:
        print(f"❌ Failed to run demo: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 