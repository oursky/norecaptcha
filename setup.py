from distutils.core import setup

from os import path

README = path.abspath(path.join(path.dirname(__file__), 'README.md'))

setup(
   name='norecaptcha',
   version='0.1',
   packages=['norecaptcha'],
   description='Python client for the google new No CAPTCHA reCAPTCHA services.',
   long_description=open(README).read(),
   author='Oursky Ltd.',
   author_email='rick.mak@gmail.com',
   url='https://github.com/oursky/norecaptcha',
   license='MIT'
)
