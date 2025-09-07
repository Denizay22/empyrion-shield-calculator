from setuptools import setup, find_packages

setup(
    name="empyrion-shield-calculator",
    version="1.0.0",
    description="Shield configuration calculator for Empyrion Galactic Survival",
    author="Denizay22",
    author_email="your.email@example.com",
    url="https://github.com/Denizay22/empyrion-shield-calculator",
    packages=find_packages(),
    package_data={
        "": ["*.json"],
    },
    install_requires=[
        "PyQt6>=6.0.0",
    ],
    entry_points={
        "console_scripts": [
            "shield-calculator=shield_calculator:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.6",
)
