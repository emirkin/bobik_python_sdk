from distutils.core import setup

requirements = ['eventlet>=0.9']

setup(
	name='Bobik Python SDK',
	version='1.0',
	packages=['bobik'],
	install_requires=requirements
)
