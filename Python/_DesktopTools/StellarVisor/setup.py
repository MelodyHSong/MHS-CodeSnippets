from setuptools import setup, find_packages

setup(
    name="stellar-visor",
    version="2.0.0",
    description="Stellar Visor - Cosmic Real-Time Desktop Network Workstation",
    author="Melody H. Song / Cassiopeia Studios",
    packages=find_packages(),
    package_data={
        "StellarVisor": ["data.json", "assets/*"],
    },
    include_package_data=True,
    install_requires=[
        "psutil>=5.9.0",
        "pillow>=10.0.0",
    ],
    entry_points={
        "gui_scripts": [
            "stellarvisor = StellarVisor.stellar_visor:main",
        ],
        "console_scripts": [
            "stellarvisor-cli = StellarVisor.__main__:main",
        ],
    },
    python_requires=">=3.8",
)
