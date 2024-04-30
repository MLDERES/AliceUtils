from setuptools import setup

setup(
    name='budget-fixup',
    version='0.1.0',
    py_modules=['budget_fixup'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'budget_fixup = budget_fixup:process_files',
        ],
    },
)