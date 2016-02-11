from setuptools import setup
import qbar

setup(
    name='qbar',
    packages=['qbar', 'qbar.items'],
    data_files=['configs/default.css', 'configs/default.py'],
    version=qbar.__version__,
    description=
    'An easily-configurable and flexible status bar for Linux',
    long_description=open('README.rst', 'r').read(),
    license='Apache License, Version 2.0',
    author='Justin Buchanan',
    author_email='justbuchanan@gmail.com',
    maintainer='Justin Buchanan',
    maintainer_email='justbuchanan@gmail',
    url='https://github.com/justbuchanan/qbar',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Development Status :: 3 - Alpha',
    ],
    entry_points={'console_scripts': ['qbar = qbar.main:main']},
    extra_requires={
        'wifi_bar_item': ['wifi'],
        'battery_bar_item': ['power'],
        'cpu_bar_item': ['psutil'],
        'alsa_volume_bar_item': ['pyalsaaudio'],
    },
    test_suite='nose.collector',
    tests_require=['nose'])
