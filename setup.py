from setuptools import setup

setup(
    name='budget_fix',
    version='0.1.0',
    py_modules=['budget_fix'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'budget_fix = budget_fix:process_files',
        ],
    },
)