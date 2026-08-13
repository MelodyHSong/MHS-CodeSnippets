# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: setup.py
# ☆ Date: 2026-08-13
# ☆
# ☆ Description: Package installation and entry point setup 
# ☆ configuration for NetworkInfo.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

from setuptools import setup, find_packages


setup(
    name="NetworkInfo",
    version="1.0.0",
    description="Real-Time Network Performance Analyzer",
    author="MelodyHSong",
    packages=find_packages(),
    package_data={
        "NetworkInfo": ["data.json"],
    },
    include_package_data=True,
    install_requires=[
        "psutil>=5.9.0",
    ],
    entry_points={
        "console_scripts": [
            "networkinfo = NetworkInfo.__main__:main",
        ],
    },
    python_requires=">=3.7",
)

