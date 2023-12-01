from setuptools import setup, find_packages

setup(
    name='lolapp',  # Name of your distribution package
    version='0.1.0',
    packages=find_packages(),  # Automatically find your packages
    entry_points={
        'console_scripts': [
            'lolapp=lolapp.lolapp:main',  # 'lolapp' command calls main() from lolapp.py inside the lolapp package
        ],
    },
    
)
