#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='siphon',
    version='0.0.1',
    author='Telmo Menezes',
    author_email='telmo@telmomenezes.net',
    description='Retrieve Reddit data.',
    url='https://github.com/telmomenezes/siphon',
    license='MIT',
    keywords=['Reddit', 'Data Science', 'Data Collection', 'Crawler',
              'Extract Data', 'Computational Social Science',
              'Computational Sociology'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Topic :: Sociology'
    ],
    python_requires='>=3.5',
    packages=find_packages(),
    install_requires=[
        'pushshift.py',
    ],
    entry_points={
        'console_scripts': [
            'siphon = siphon.__main__:cli',
        ],
    }
)
