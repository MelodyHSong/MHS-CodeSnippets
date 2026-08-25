from setuptools import setup, find_packages

setup(
    name="NetworkInfo",
    version="1.0.0",
    description="Kaomoji Real-Time Network Performance Analyzer (Alien HUD)",
    author="Antigravity AI",
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
