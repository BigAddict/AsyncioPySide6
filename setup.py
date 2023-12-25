# setup.py
from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='AsyncioPySide6',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'PySide6',
    ],
    entry_points={},
    test_suite='tests',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
