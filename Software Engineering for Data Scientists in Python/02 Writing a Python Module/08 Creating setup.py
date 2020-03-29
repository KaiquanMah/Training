Creating setup.py
In order to make your package installable by pip you need to create a setup.py file. In this exercise you will create this file for the text_analyzer package you've been building.

import the needed function, setup, from the setuptools package.
Complete the name & packages arguments; keep in mind your package is located in a directory named text_analyzer.
List yourself as the author.





# Import needed function from setuptools
from setuptools import setup

# Create proper setup to be used by pip
setup(name='text_analyzer',
      version='0.0.1',
      description='Perform and visualize a text anaylsis.',
      author='kai',
      packages=['text_analyzer'])




<script.py> output:
    running bdist_rpm
    running egg_info
    creating text_analyzer.egg-info
    writing text_analyzer.egg-info/PKG-INFO
    writing dependency_links to text_analyzer.egg-info/dependency_links.txt
    writing top-level names to text_analyzer.egg-info/top_level.txt
    writing manifest file 'text_analyzer.egg-info/SOURCES.txt'
    reading manifest file 'text_analyzer.egg-info/SOURCES.txt'
    writing manifest file 'text_analyzer.egg-info/SOURCES.txt'
    creating dist
    writing 'dist/text_analyzer.spec'
    
    
Perfect! Thanks to creating this setup.py file you can now pip install your package and even publish it to PyPi!

    
