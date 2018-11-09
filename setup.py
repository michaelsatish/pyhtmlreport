from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
	name='pyhtmlreport',
	version='1.0',
	packages=['pyhtmlreport'],
	package_data = {'pyhtmlreport': ['templates/*']},
	description='Implement html reporting in Test Automation',
	long_description=long_description,
	author='Satish Kumar Kadarkarai Mani',
	author_email='michael.satish@gmail.com',
	url='https://github.com/michaelsatish/pyhtmlreport',
	install_requires=[
		'Pillow>=5.3.0',
		'jinja2>=2.10'
	],
	keywords='html report',
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'Operating System :: POSIX',
		'Operating System :: Microsoft :: Windows',
		'Operating System :: MacOS :: MacOS X',
		'Topic :: Software Development :: Quality Assurance',
		'Topic :: Software Development :: Testing',
		'Topic :: Utilities',
		'Programming Language :: Python :: 3.7'
	]
)
