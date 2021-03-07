"""
Rare Number Generator
"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rare-numbers',  # Required

    version='0.1.0',

    description='Rare Numbers in Python',

    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ajs/rare-numbers',
    author='Aaron Sherman',
    author_email='ajs@ajs.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='rare-numbers math mathematics tool',

    packages=find_packages(exclude=['tests']),

    python_requires='>=3.5, <4',
    install_requires=[''],
    extras_require={  # Optional
        'dev': ['pytest>=6.2.2,<6.3'],
        'test': ['pytest>=6.2.2,<6.3'],
    },
    entry_points={
        'console_scripts': [
            'rare-numbers=rare_num:main',
        ],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/ajs/rare-numbers/issues',
        'Source': 'https://github.com/ajs/rare-numbers/',
    },
)
