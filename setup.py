# setup.py

from setuptools import setup, find_packages

setup(
    name="SmartFridge",                    # Name of your package
    version="0.1",                         # Initial version
    description="An IoT-based smart fridge project",  # Short description
    author="Filippo Gibertini",                    # Your name or organization
    author_email="...", # Your contact email
    packages=find_packages(where="."),              # Automatically find all packages
    package_dir={
        'src': 'src',
        'utility': 'utility',
    },
    install_requires=[
        'opencv-python', 
        'requests',
        'pyzbar'
    ],
    entry_points={
        'console_scripts': [
            'smart_fridge=src.main:main',  # Optional CLI entry point
        ],
    },
)
