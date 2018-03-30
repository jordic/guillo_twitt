from setuptools import find_packages
from setuptools import setup


try:
    README = open('README.rst').read()
except IOError:
    README = None

setup(
    name='guillo_twitt',
    version="1.0.0",
    description='A Service for twitting content items',
    long_description=README,
    install_requires=[
        'guillotina',
        'aioauth-client==0.10.0'
    ],
    author='jordi',
    author_email='j@tmpo.io',
    url='',
    packages=find_packages(exclude=['demo']),
    include_package_data=True,
    tests_require=[
        'pytest',
    ],
    extras_require={
        'test': [
            'pytest'
        ]
    },
    classifiers=[],
    entry_points={
    }
)
