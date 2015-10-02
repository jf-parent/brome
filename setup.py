#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = []

with open('requirements.txt', 'r') as fd:
    for line in fd:
        requirements.append(line)

setup(
    name='brome',
    version='0.0.5',
    description="Framework For Selenium",
    long_description=readme,
    author="Brome-HQ",
    author_email='brome.hq@gmail.com',
    url='https://github.com/brome-hq/brome',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='brome',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ]
)
