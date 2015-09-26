from setuptools import setup
import qbar

setup(
    name='qbar',
    packages=['qbar', 'qbar.items'],
    data_files=['qbar-default.css', 'qbar-default.yml'],
    version=qbar.__version__,
    description=
    'An easily-configurable and flexible status bar for Linux',
    long_description=open('readme.rst', 'r').read(),
    license='Apache License, Version 2.0',
    author='Justin Buchanan',
    author_email='justbuchanan@gmail.com',
    maintainer='Justin Buchanan',
    maintainer_email='justbuchanan@gmail',
    url='https://github.com/justbuchanan/qbar',
    classifiers=['Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4'],
    entry_points={'console_scripts': ['qbar = qbar.main:main']},
    install_requires=['power', 'wifi'],
    test_suite='nose.collector',
    tests_require=['nose'])
