"""
A python package for interfacing with the Omniture Web Services API.
"""
import re
from setuptools import setup, find_packages
from codecs import open
from os import path

d = path.abspath(path.dirname(__file__))

setup(
    name='omniture',

    version='0.0.4',

    description=(
        'A python package for interfacing with the Omniture Web Services API ' +
        '(https://marketing.adobe.com/developer/documentation).'
    ),

    # The project's main homepage.
    url='https://tools.adidas-group.com/bitbucket/projects/USDA/repos/omniture/browse',

    # Author details
    author='Stephen Knoth',
    author_email='stephen.kntoh@adidas.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='omniture adobe analytics',

    packages=find_packages(exclude=['docs', 'tests']),
    # packages=[], # explicitly set packages
    # py_modules=[], # Single-file module names

    # dependencies
    # See https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        "future>=0.17.0"
    ],

    # pip install -e .[dev,test]
    extras_require={
        'dev': ['pytest>=2.9.0'],
        'test': ['pytest>=2.9.0'],
    },

    package_data={},

    # See http://docs.python.org/3.5/distutils/setupscript.html#installing-additional-files
    data_files=[],

    entry_points={
        'console_scripts': [],
    }
)
