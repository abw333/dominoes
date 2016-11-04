from setuptools import setup

setup(
    name='domino',
    version='0.0.0',
    description='Python implementation of the dominoes game.',
    url='https://github.com/abw333/domino',
    author='Alan Wagner',
    author_email='alanwagner333@gmail.com',
    packages=['domino'],
    install_requires=['numpy>=1.11.2'],
    test_suite='tests'
)
