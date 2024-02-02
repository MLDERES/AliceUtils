from setuptools import setup

setup(
    name='cleaner',
    version='0.1.0',
    py_modules=['cleaner'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'cleaner = cleaner:process_files',
        ],
    },
)