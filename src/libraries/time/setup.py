#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools

with open("README.rst", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='python-time',
    version='0.3.0',
    author='binary',
    author_email='nothing_style@126.com',
    description='sample time module',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=['arrow'],
    url='https://github.com/hengdai/pytime',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)


