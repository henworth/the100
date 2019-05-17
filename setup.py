import re
from distutils.core import setup

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = ''
with open('the100.py') as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

setup(name='the100',
      author='Michael Hennessy',
      author_email='henworth@henabytes.com',
      version=version,
      license='MIT',
      description='An asynchronous Python client for accessing the100.io API',
      install_requires=requirements,
      py_modules=['the100'])
