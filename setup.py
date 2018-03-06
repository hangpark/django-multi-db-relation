#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from io import open

from setuptools import find_packages, setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('multi_db_relation')


setup(
    name='django-multi-db-relation',
    version=version,
    url='https://github.com/hangpark/django-multi-db-relation',
    license='BSD',
    description='Django query optimization supports for multi db relations.',
    long_description=open('README.md').read(),
    author='Hang Park',
    author_email='hangpark@kaist.ac.kr',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=[
        'Django>=1.10',
    ],
    python_requires=">=3.5",
    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
    ]
)
