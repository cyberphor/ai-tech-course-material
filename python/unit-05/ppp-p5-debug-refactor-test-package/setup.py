from setuptools import setup

setup(name='shoppinglistapp',
      version='1.0.0',
      description='Addition and Subtraction Practice App',
      url='https://whatever.org/',
      author='Victor Fernandez',
      author_email='vf@andrew.cmu.edu',
      packages=['shoppinglistapp', 'shoppinglistapp.core'],
      include_package_data=True,
      zip_safe=False)