from setuptools import setup

setup(
    name='nail',
    version='0.1',
    py_modules=['main', 'app'],
    install_requires=[
        'click',
        'openai'
    ],
    entry_points='''
        [console_scripts]
        nail=main:main
    ''',
)
