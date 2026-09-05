from setuptools import setup, find_packages

setup(
    name="NetworkInfo",
    version="2.0.0",
    description="Melody's Starship Network Visor - Cosmic Real-Time Desktop Network Workstation",
    author="Melody H. Song / Cassiopeia Studios",
    packages=find_packages(),
    package_data={
        "NetworkInfo": ["data.json", "assets/*"],
    },
    include_package_data=True,
    install_requires=[
        "psutil>=5.9.0",
        "pillow>=10.0.0",
    ],
    entry_points={
        "gui_scripts": [
            "networkvisor = NetworkInfo.network_info:main",
        ],
        "console_scripts": [
            "networkinfo = NetworkInfo.__main__:main",
        ],
    },
    python_requires=">=3.8",
)
