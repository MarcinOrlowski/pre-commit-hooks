#
# pre-commit-hooks
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/pre-commit-hooks/
#

from setuptools import find_packages
from setuptools import setup

setup(
    name = 'hooks',
    description = 'Some useful Git hooks for pre-commit',
    url = 'https://github.com/MarcinOrlowski/pre-commit-hooks',
    version = '1.2.2',

    author = 'Marcin Orlowski',

    platforms = 'linux',
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    packages = find_packages('.'),
    install_requires = [],
    entry_points = {
        'console_scripts': [
            'mor-checkstyle-jar = hooks.checkstyle_jar:main',
            'mor-trailing-whitespaces = hooks.trailing_whitespaces:main',
            'mor-end-of-file = hooks.end_of_file:main',
            'mor-no-op = hooks.no_op:main',
        ],
    },
)
