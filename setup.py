#!/usr/bin/python3

import codecs
from setuptools import setup, find_packages


with codecs.open("README.rst", encoding="utf8") as readme_f:
    README = readme_f.read()

setup(
    name="srt3",
    version="1.0.0",
    python_requires=">=3.3",
    description="A simple library for parsing, modifying, and composing SRT files.",
    long_description=README,
    long_description_content_type="text/x-rst",
    author="SwitchUpCB",
    url="https://github.com/switchupcb/srt3",
    packages=find_packages(include=["srt", "srt.*"]),
    license="MIT",
    license_files=("LICENSE"),
    keywords=["srt", "srt3"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries",
        "Topic :: Text Processing",
    ],
    entry_points={
        "console_scripts": [
            "srt = srt.tools._srt:main",
        ],
    },
)
