from setuptools import setup, find_packages
from codecs import open 
from os import path

here = path.abspath(path.dirname(__file__))

setup(
  name = 'twarkov',
  version = '0.0.1',
  description = 'Markov generator built for generating Tweets from timelines',
  license = 'MIT',
  author = 'Amanda Pickering',
  author_email = 'pickering.amanda@gmail.com',
  install_requires = ['nltk', 'wsgiref'],
  url = 'https://github.com/amandapickering/twarkov',
  keywords = 'twitter markov generator bots',
  packages = find_packages(),
)
