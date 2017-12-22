from setuptools import setup

setup(
	name='pyhtmlreport',
	version='1.0',
	packages=['pyhtmlreport'],
	package_data = {'pyhtmlreport': ['data/*']},
	description='A python library to implement html test reporting',
	author='Satish Kumar Kadarkarai Mani',
	author_email='michael.satish@gmail.com',
	install_requires=['Pillow>=4.3.0']
	)