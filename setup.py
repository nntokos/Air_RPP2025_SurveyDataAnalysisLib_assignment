from setuptools import setup, find_packages

setup(
    name="so_surveyanalysis",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "openpyxl",
        "argparse",
        "pytest",
        "tabulate",
    ],
    entry_points={
        "console_scripts": [
            "so_surveyanalysis=so_surveyanalysis.cli:main",
        ],
    },
    description="A library for analyzing Stack Overflow survey data",
    author="Nikolaos Ntokos",
    author_email="ndokos@hotmail.com",
    url="https://github.com/nntokos/so_surveyanalysis",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)