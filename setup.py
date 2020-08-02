# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in graphene_frappe/__init__.py
from graphene_frappe import __version__ as version

setup(
	name='graphene_frappe',
	version=version,
	description='Frappe integration with Graphene',
	author='Ahmad Ragheb',
	author_email='ahmadragheb75@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
