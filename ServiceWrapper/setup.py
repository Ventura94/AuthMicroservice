"""
Setup
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Service Wrapper",
    version="0.0.1",
    author="Arian Ventura Rodríguez",
    author_email="arianventura94@gmail.com",
    description="Service Wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ventura94/ServiceWrapper",
    project_urls={
        "Bug Tracker": "https://github.com/ventura94/ServiceWrapper/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "service_wrapper"},
    packages=setuptools.find_packages(where="service_wrapper"),
    python_requires=">=3.6",
)
