from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='nail',
    version='0.1.0',
    description='A CLI tool for speeding up development using LLMs',
    py_modules=['main', 'app'],
    install_requires=[
        'click',
        'openai'
    ],
    entry_points='''
        [console_scripts]
        nail=main:main
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
