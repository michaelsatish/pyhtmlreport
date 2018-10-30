from setuptools import setup

setup(
	name='pyhtmlreport',
	version='1.0',
	packages=['pyhtmlreport'],
	package_data = {'pyhtmlreport': ['templates/*']},
	description='python library to implement html reporting',
	author='Satish Kumar Kadarkarai Mani',
	author_email='michael.satish@gmail.com',
	install_requires=[
		'Pillow>=5.3.0',
		'jinja2>=2.10'
		]
	)