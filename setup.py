from distutils.core import setup

requirements = ['requests>=0.12']

setup(
	name='bobik_python_sdk',
	version='1.0',
	packages=['bobik'],
	url='https://github.com/emirkin/bobik_python_sdk',
	author='Eugene Mirkin',
	author_email='support@usebobik.com',
	install_requires=requirements
)
