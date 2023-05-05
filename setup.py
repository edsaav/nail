from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='nail',
    version='0.1.1',
    description='A CLI tool for speeding up development using LLMs',
    packages=find_packages(),
    install_requires=[
        'click',
        'openai',
        'termcolor',
        'PyYAML',
    ],
    entry_points='''
        [console_scripts]
        nail=nail.main:main
    ''',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Edward Saavedra',
    author_email='edsaav@gmail.com',
    url='https://github.com/edsaav/nail',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
