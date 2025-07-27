Basic Example
=============

This example demonstrates the fundamental features of AsyncioPySide6 including basic async task execution, timeout handling, retry logic, and GUI thread safety.

Overview
--------

The basic example shows how to:

* Initialize AsyncioPySide6 with a Qt application
* Run simple async tasks
* Handle timeouts gracefully
* Implement retry logic for flaky operations
* Ensure thread-safe GUI updates

Code Example
------------

.. literalinclude:: ../../../examples/basic_example.py
   :language: python
   :caption: Basic Example (examples/basic_example.py)

Key Features Demonstrated
-------------------------

Basic Task Execution
^^^^^^^^^^^^^^^^^^^^

The example starts with a simple async task that simulates work:

.. code-block:: python

   async def simple_task():
       print("Starting simple task...")
       await asyncio.sleep(2)
       print("Simple task completed!")

   AsyncioPySide6.runTask(simple_task())

Timeout Handling
^^^^^^^^^^^^^^^^

Demonstrates how to handle tasks that might take too long:

.. code-block:: python

   async def timeout_task():
       print("Starting timeout task...")
       await asyncio.sleep(5)  # This will timeout after 3 seconds
       print("Timeout task completed!")

   AsyncioPySide6.runTaskWithTimeout(timeout_task(), timeout=3.0)

Retry Logic
^^^^^^^^^^^^

Shows how to handle flaky operations with automatic retries:

.. code-block:: python

   async def retry_task():
       if random.random() < 0.7:  # 70% chance of failure
           raise Exception("Random failure")
       return "Success!"

   AsyncioPySide6.runTaskWithRetry(
       lambda: retry_task(),
       max_retries=3,
       retry_delay=1.0
   )

Thread-Safe GUI Updates
^^^^^^^^^^^^^^^^^^^^^^^^

Demonstrates safe GUI updates from async tasks:

.. code-block:: python

   def update_label(text):
       label.setText(text)

   async def gui_task():
       await asyncio.sleep(1)
       AsyncioPySide6.invokeInGuiThread(label, lambda: update_label("Updated from async task!"))

Running the Example
-------------------

To run the basic example:

.. code-block:: bash

   cd examples
   python basic_example.py

Expected Output
---------------

The example will show:

* Simple task execution with timing
* Timeout handling with appropriate error messages
* Retry logic with success after failures
* Thread-safe GUI updates
* Performance metrics and health status

This example provides a foundation for understanding how AsyncioPySide6 integrates async programming with Qt applications while maintaining thread safety and providing robust error handling. 