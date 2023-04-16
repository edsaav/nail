from setuptools import setup

setup(
    name='skink',
    version='0.1',
    py_modules=['main', 'app'],
    install_requires=[
        'click',
        'openai'
    ],
    entry_points='''
        [console_scripts]
        skink=main:main
    ''',
)
