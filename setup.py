import re
from setuptools import setup

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = ''
with open('the100.py') as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='the100',
    author="Michael Hennessy",
    author_email='henworth@henabytes.com',
    version=version,
    license='MIT',
    description="An asynchronous Python client for accessing the100.io API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/henworth/the100',
    install_requires=requirements,
    py_modules=['the100'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
