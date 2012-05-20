#from distutils.core import setup
from setuptools import setup

setup(name='restdoc',
      version='0.0.1',
      author="Stephen Sugden",
      author_email="glurgle@gmail.com",
      packages=['restdoc'],
      requires=['prettytable (==0.6)',
                'urllib3 (==1.3)',
               ]
      )
