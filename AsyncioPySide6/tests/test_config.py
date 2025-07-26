"""
Tests for the AsyncioPySide6 configuration system.
"""

import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
from AsyncioPySide6.nvd.config import (
    AsyncioPySide6Config,
    get_config,
    set_config,
    reset_config
)


class TestAsyncioPySide6Config(unittest.TestCase):
    """Test suite for AsyncioPySide6Config"""
    
    def setUp(self):
        """Set up test environment"""
        # Reset configuration before each test
        reset_config()
    
    def tearDown(self):
        """Clean up after each test"""
        # Reset configuration after each test
        reset_config()
    
    def test_default_configuration(self):
        """Test default configuration values"""
        config = AsyncioPySide6Config()
        
        # Test default values
        self.assertEqual(config.event_loop_interval, 0.01)  # Updated for better stability
        self.assertEqual(config.idle_sleep_time, 0.01)      # Updated for better stability
        self.assertTrue(config.use_dedicated_thread)        # Updated for better thread safety
        self.assertEqual(config.initialization_timeout, 5.0)
        self.assertEqual(config.shutdown_timeout, 10.0)
        self.assertEqual(config.task_timeout, 30.0)
        self.assertEqual(config.max_retries, 3)
        self.assertEqual(config.retry_delay, 0.1)
        self.assertTrue(config.enable_logging)
        self.assertEqual(config.log_level, "INFO")
        self.assertEqual(config.max_concurrent_tasks, 100)
        self.assertEqual(config.task_queue_size, 1000)
        self.assertFalse(config.enable_debug_mode)
        self.assertFalse(config.enable_performance_monitoring)
    
    def test_custom_configuration(self):
        """Test custom configuration values"""
        config = AsyncioPySide6Config(
            event_loop_interval=0.002,
            idle_sleep_time=0.002,
            use_dedicated_thread=True,
            initialization_timeout=10.0,
            shutdown_timeout=20.0,
            task_timeout=60.0,
            max_retries=5,
            retry_delay=0.5,
            enable_logging=False,
            log_level="DEBUG",
            max_concurrent_tasks=200,
            task_queue_size=2000,
            enable_debug_mode=True,
            enable_performance_monitoring=True
        )
        
        # Test custom values
        self.assertEqual(config.event_loop_interval, 0.002)
        self.assertEqual(config.idle_sleep_time, 0.002)
        self.assertTrue(config.use_dedicated_thread)
        self.assertEqual(config.initialization_timeout, 10.0)
        self.assertEqual(config.shutdown_timeout, 20.0)
        self.assertEqual(config.task_timeout, 60.0)
        self.assertEqual(config.max_retries, 5)
        self.assertEqual(config.retry_delay, 0.5)
        self.assertFalse(config.enable_logging)
        self.assertEqual(config.log_level, "DEBUG")
        self.assertEqual(config.max_concurrent_tasks, 200)
        self.assertEqual(config.task_queue_size, 2000)
        self.assertTrue(config.enable_debug_mode)
        self.assertTrue(config.enable_performance_monitoring)
    
    def test_configuration_validation(self):
        """Test configuration validation"""
        # Test invalid event_loop_interval
        with self.assertRaises(ValueError):
            AsyncioPySide6Config(event_loop_interval=0)
        
        with self.assertRaises(ValueError):
            AsyncioPySide6Config(event_loop_interval=-1)
        
        # Test invalid idle_sleep_time
        with self.assertRaises(ValueError):
            AsyncioPySide6Config(idle_sleep_time=0)
        
        with self.assertRaises(ValueError):
            AsyncioPySide6Config(idle_sleep_time=-1)
        
        # Test invalid initialization_timeout
        with self.assertRaises(ValueError):
            AsyncioPySide6Config(initialization_timeout=0)
        
        with self.assertRaises(ValueError):
            AsyncioPySide6Config(initialization_timeout=-1)
        
        # Test invalid shutdown_timeout
        with self.assertRaises(ValueError):
            AsyncioPySide6Config(shutdown_timeout=0)
        
        with self.assertRaises(ValueError):
            AsyncioPySide6Config(shutdown_timeout=-1)
        
        # Test invalid task_timeout
        with self.assertRaises(ValueError):
            AsyncioPySide6Config(task_timeout=0)
        
        with self.assertRaises(ValueError):
            AsyncioPySide6Config(task_timeout=-1)
        
        # Test invalid max_retries
        with self.assertRaises(ValueError):
            AsyncioPySide6Config(max_retries=-1)
        
        # Test invalid retry_delay
        with self.assertRaises(ValueError):
            AsyncioPySide6Config(retry_delay=-1)
        
        # Test invalid max_concurrent_tasks
        with self.assertRaises(ValueError):
            AsyncioPySide6Config(max_concurrent_tasks=0)
        
        with self.assertRaises(ValueError):
            AsyncioPySide6Config(max_concurrent_tasks=-1)
        
        # Test invalid task_queue_size
        with self.assertRaises(ValueError):
            AsyncioPySide6Config(task_queue_size=0)
        
        with self.assertRaises(ValueError):
            AsyncioPySide6Config(task_queue_size=-1)
    
    def test_from_environment(self):
        """Test configuration from environment variables"""
        # Set environment variables
        env_vars = {
            'ASYNCIOPYSIDE6_EVENT_LOOP_INTERVAL': '0.002',
            'ASYNCIOPYSIDE6_IDLE_SLEEP_TIME': '0.002',
            'ASYNCIOPYSIDE6_USE_DEDICATED_THREAD': 'true',
            'ASYNCIOPYSIDE6_INIT_TIMEOUT': '10.0',
            'ASYNCIOPYSIDE6_SHUTDOWN_TIMEOUT': '20.0',
            'ASYNCIOPYSIDE6_TASK_TIMEOUT': '60.0',
            'ASYNCIOPYSIDE6_MAX_RETRIES': '5',
            'ASYNCIOPYSIDE6_RETRY_DELAY': '0.5',
            'ASYNCIOPYSIDE6_ENABLE_LOGGING': 'false',
            'ASYNCIOPYSIDE6_LOG_LEVEL': 'DEBUG',
            'ASYNCIOPYSIDE6_MAX_CONCURRENT_TASKS': '200',
            'ASYNCIOPYSIDE6_TASK_QUEUE_SIZE': '2000',
            'ASYNCIOPYSIDE6_ENABLE_DEBUG_MODE': 'true',
            'ASYNCIOPYSIDE6_ENABLE_PERFORMANCE_MONITORING': 'true'
        }
        
        with patch.dict(os.environ, env_vars):
            config = AsyncioPySide6Config.from_environment()
            
            # Test environment variable values
            self.assertEqual(config.event_loop_interval, 0.002)
            self.assertEqual(config.idle_sleep_time, 0.002)
            self.assertTrue(config.use_dedicated_thread)
            self.assertEqual(config.initialization_timeout, 10.0)
            self.assertEqual(config.shutdown_timeout, 20.0)
            self.assertEqual(config.task_timeout, 60.0)
            self.assertEqual(config.max_retries, 5)
            self.assertEqual(config.retry_delay, 0.5)
            self.assertFalse(config.enable_logging)
            self.assertEqual(config.log_level, "DEBUG")
            self.assertEqual(config.max_concurrent_tasks, 200)
            self.assertEqual(config.task_queue_size, 2000)
            self.assertTrue(config.enable_debug_mode)
            self.assertTrue(config.enable_performance_monitoring)
    
    def test_from_environment_partial(self):
        """Test configuration from partial environment variables"""
        # Set only some environment variables
        env_vars = {
            'ASYNCIOPYSIDE6_EVENT_LOOP_INTERVAL': '0.002',
            'ASYNCIOPYSIDE6_USE_DEDICATED_THREAD': 'true',
            'ASYNCIOPYSIDE6_LOG_LEVEL': 'DEBUG'
        }
        
        with patch.dict(os.environ, env_vars):
            config = AsyncioPySide6Config.from_environment()
            
            # Test that set values are used
            self.assertEqual(config.event_loop_interval, 0.002)
            self.assertTrue(config.use_dedicated_thread)
            self.assertEqual(config.log_level, "DEBUG")
            
            # Test that unset values use defaults
            self.assertEqual(config.idle_sleep_time, 0.01)  # Updated default
            self.assertEqual(config.initialization_timeout, 5.0)
            self.assertEqual(config.shutdown_timeout, 10.0)
            self.assertEqual(config.task_timeout, 30.0)
            self.assertEqual(config.max_retries, 3)
            self.assertEqual(config.retry_delay, 0.1)
            self.assertTrue(config.enable_logging)
            self.assertEqual(config.max_concurrent_tasks, 100)
            self.assertEqual(config.task_queue_size, 1000)
            self.assertFalse(config.enable_debug_mode)
            self.assertFalse(config.enable_performance_monitoring)
    
    def test_to_dict(self):
        """Test configuration to dictionary conversion"""
        config = AsyncioPySide6Config(
            event_loop_interval=0.002,
            use_dedicated_thread=True,
            log_level="DEBUG"
        )
        
        config_dict = config.to_dict()
        
        # Test that all values are present
        self.assertIn('event_loop_interval', config_dict)
        self.assertIn('idle_sleep_time', config_dict)
        self.assertIn('use_dedicated_thread', config_dict)
        self.assertIn('initialization_timeout', config_dict)
        self.assertIn('shutdown_timeout', config_dict)
        self.assertIn('task_timeout', config_dict)
        self.assertIn('max_retries', config_dict)
        self.assertIn('retry_delay', config_dict)
        self.assertIn('enable_logging', config_dict)
        self.assertIn('log_level', config_dict)
        self.assertIn('log_format', config_dict)
        self.assertIn('max_concurrent_tasks', config_dict)
        self.assertIn('task_queue_size', config_dict)
        self.assertIn('enable_debug_mode', config_dict)
        self.assertIn('enable_performance_monitoring', config_dict)
        
        # Test that custom values are correct
        self.assertEqual(config_dict['event_loop_interval'], 0.002)
        self.assertEqual(config_dict['use_dedicated_thread'], True)
        self.assertEqual(config_dict['log_level'], "DEBUG")
        
        # Test that default values are correct
        self.assertEqual(config_dict['idle_sleep_time'], 0.01)  # Updated default
        self.assertEqual(config_dict['initialization_timeout'], 5.0)
        self.assertEqual(config_dict['shutdown_timeout'], 10.0)
    
    def test_str_representation(self):
        """Test string representation of configuration"""
        config = AsyncioPySide6Config(
            event_loop_interval=0.002,
            use_dedicated_thread=True
        )
        
        config_str = str(config)
        
        # Test that the string contains key information
        self.assertIn("AsyncioPySide6Config", config_str)
        self.assertIn("event_loop_interval=0.002", config_str)
        self.assertIn("use_dedicated_thread=True", config_str)
    
    def test_logging_setup(self):
        """Test that logging is properly set up"""
        # Test with logging enabled
        config = AsyncioPySide6Config(
            enable_logging=True,
            log_level="DEBUG"
        )
        
        # The logging should be set up in __post_init__
        # We can't easily test the actual logging setup without complex mocking
        # but we can test that the configuration is correct
        self.assertTrue(config.enable_logging)
        self.assertEqual(config.log_level, "DEBUG")
        
        # Test with logging disabled
        config = AsyncioPySide6Config(
            enable_logging=False
        )
        
        self.assertFalse(config.enable_logging)


class TestConfigFunctions(unittest.TestCase):
    """Test suite for configuration functions"""
    
    def setUp(self):
        """Set up test environment"""
        reset_config()
    
    def tearDown(self):
        """Clean up after each test"""
        reset_config()
    
    def test_get_config_default(self):
        """Test getting default configuration"""
        config = get_config()
        
        # Should return default configuration
        self.assertIsInstance(config, AsyncioPySide6Config)
        self.assertEqual(config.event_loop_interval, 0.01)  # Updated default
        self.assertTrue(config.use_dedicated_thread)        # Updated default
    
    def test_set_config(self):
        """Test setting custom configuration"""
        custom_config = AsyncioPySide6Config(
            event_loop_interval=0.002,
            use_dedicated_thread=True
        )
        
        set_config(custom_config)
        
        # Should return the custom configuration
        config = get_config()
        self.assertEqual(config.event_loop_interval, 0.002)
        self.assertTrue(config.use_dedicated_thread)
    
    def test_reset_config(self):
        """Test resetting configuration"""
        # Set custom configuration
        custom_config = AsyncioPySide6Config(
            event_loop_interval=0.002,
            use_dedicated_thread=True
        )
        set_config(custom_config)
        
        # Reset configuration
        reset_config()
        
        # Should return default configuration
        config = get_config()
        self.assertEqual(config.event_loop_interval, 0.01)  # Updated default
        self.assertTrue(config.use_dedicated_thread)        # Updated default
    
    def test_config_singleton_behavior(self):
        """Test that configuration behaves like a singleton"""
        config1 = get_config()
        config2 = get_config()
        
        # Should return the same instance
        self.assertIs(config1, config2)
        
        # Modifying one should affect the other
        config1.event_loop_interval = 0.002
        self.assertEqual(config2.event_loop_interval, 0.002)
    
    def test_environment_integration(self):
        """Test integration with environment variables"""
        env_vars = {
            'ASYNCIOPYSIDE6_EVENT_LOOP_INTERVAL': '0.002',
            'ASYNCIOPYSIDE6_USE_DEDICATED_THREAD': 'true'
        }
        
        with patch.dict(os.environ, env_vars):
            # Reset to ensure environment is read
            reset_config()
            
            config = get_config()
            self.assertEqual(config.event_loop_interval, 0.002)
            self.assertTrue(config.use_dedicated_thread)


if __name__ == '__main__':
    unittest.main() 