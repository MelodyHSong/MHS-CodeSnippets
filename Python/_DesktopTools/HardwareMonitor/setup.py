from setuptools import setup, find_packages

setup(
    name="HardwareMonitor",
    version="1.0.0",
    description="Kaomoji Real-Time Hardware Performance & Responsiveness Analyzer HUD",
    author="MelodyHSong",
    packages=find_packages(),
    package_data={
        "HardwareMonitor": ["data.json"],
    },
    include_package_data=True,
    install_requires=[
        "psutil>=5.9.0",
    ],
    entry_points={
        "console_scripts": [
            "hardwaremonitor = HardwareMonitor.__main__:main",
        ],
    },
    python_requires=">=3.7",
)
