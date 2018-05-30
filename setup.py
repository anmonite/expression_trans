# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='expression_trans',
    version='0.2.0',
    description='This package is to translate Japanese text along the expression converting model with using Sudachi as a morphological tokenizer.',
    long_description=readme,
    author='Norihiro Matsushita',
    author_email='night77@gmail.com',
    url='https://github.com/anmonite/',
    license=license,
    install_requires=[],
    dependency_links=['git+ssh:github.com/WorksApplications/SudachiPy.git#egg=sudachipy'],
    packages=find_packages(exclude=('tests', 'docs'))
)

