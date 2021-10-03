import setuptools
from setuptools import find_packages

def readme():
    with open('README.md') as f:
        return f.read()
setuptools.setup(
    name='amwater',
    version='0.0.3',
    packages=find_packages(),
    url='https://github.com/samapriya/amwater',
    install_requires=['requests>=2.26.0',
    'lxml>=4.6.3',
    'beautifulsoup4>=4.9.3',
    'dateparser>=1.0.0',
    'shapely>=1.6.4;platform_system!="Windows"',],
    license='Apache 2.0',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: GIS',
    ],
    author='Samapriya Roy',
    author_email='samapriya.roy@gmail.com',
    description='Alert CLI for American water',
    entry_points={
        'console_scripts': [
            'amwater=amwater.amwater:main',
        ],
    },
)

