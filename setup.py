#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', 'hypothesis', ]

doc_requirements = ['Sphinx==1.7.1', ]

setup(
    author="Sahin Kureta",
    author_email='skureta@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    description="Collection of tools for Ircam's OpenMusic.",
    entry_points={
        'console_scripts': [
            'pytom=pytom.cli:main',
        ],
    },
    install_requires=requirements,
    extras_require={
        'docs': doc_requirements
    },
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pytom',
    name='pytom',
    packages=find_packages(include=['pytom']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/kureta/pytom',
    version='0.1.6',
    zip_safe=False,
)
