"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path


here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pohjala-scripts',
    version='0.0.0',
    description='Erinevad skriptid, mis lahendavad korduvaid EÜS Põhjala '
                'andmetega seotud probleeme.',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/kendas/pohjala-scripts',
    author='Kaarel Ratas',
    author_email='kaarel.ratas@gmail.com',

    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Intended Audience :: End Users/Desktop',
        'Topic :: Education',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='sample setuptools development',  # Optional
    packages=find_packages(),  # Required
    install_requires=[
        'tabulate',
    ],
    entry_points={  # Optional
        'console_scripts': [
            'kopeeri-liikmed=pscripts.liikmed:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/kendas/pohjala-scripts/issues',
        'Source': 'https://github.com/kendas/pohjala-scripts/',
    },
)
