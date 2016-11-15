from setuptools import setup

setup(
    name='dominoes',
    version='0.0.0',
    description='A Python library for the dominoes game.',
    url='https://github.com/abw333/dominoes',
    author='Alan Wagner',
    author_email='alanwagner333@gmail.com',
    license='MIT',
    packages=['dominoes'],
    scripts=['bin/dominoes'],
    test_suite='tests'
)
