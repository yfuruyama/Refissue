# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='scripts',
    py_modules=[
        'create_hook'
        ],
    entry_points={
        'console_scripts': [
            'create_hook = create_hook:main'
            ]
        })
