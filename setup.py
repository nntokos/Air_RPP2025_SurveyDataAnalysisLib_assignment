# setup.py

from setuptools import setup, find_packages

setup(
    name="so_surveyanalysis",
    version="0.1.0",
    description="A CLI and library for analyzing Stack Overflow survey data",
    author="Nikos Ntokos",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "openpyxl>=3.1.0",
        "tabulate>=0.8.9"
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "so_surveyanalysis=so_surveyanalysis.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)