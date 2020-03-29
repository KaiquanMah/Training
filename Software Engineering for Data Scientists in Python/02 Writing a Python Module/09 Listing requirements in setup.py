Listing requirements in setup.py
We created a setup.py file earlier, but we forgot to list our dependency on matplotlib in the install_requires argument. In this exercise you will practice listing your version specific dependencies by correcting the setup.py you previously wrote for your text_analyzer package.

import the needed function, setup, from the setuptools package.
List yourself as the author.
Specify your install_requires to require matplotlib version 3.0.0 or above.


# Import needed function from setuptools
from setuptools import setup

# Create proper setup to be used by pip
setup(name='text_analyzer',
      version='0.0.1',
      description='Perform and visualize a text anaylsis.',
      author='kai',
      packages=['text_analyzer'],
      install_requires=['matplotlib>=3.0.0'])


<script.py> output:
    running bdist_rpm
    running egg_info
    creating text_analyzer.egg-info
    writing text_analyzer.egg-info/PKG-INFO
    writing requirements to text_analyzer.egg-info/requires.txt
    writing dependency_links to text_analyzer.egg-info/dependency_links.txt
    writing top-level names to text_analyzer.egg-info/top_level.txt
    writing manifest file 'text_analyzer.egg-info/SOURCES.txt'
    reading manifest file 'text_analyzer.egg-info/SOURCES.txt'
    writing manifest file 'text_analyzer.egg-info/SOURCES.txt'
    creating dist
    writing 'dist/text_analyzer.spec'
    
    Package setup for text_analyzer by kai was succesful!
    
    
Great work! When users pip install your package the correct version of matplotlib will be automatically handled by pip.

    
