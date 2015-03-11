from distutils.core import setup

from os import path

README = path.abspath(path.join(path.dirname(__file__), 'README.md'))

setup(
   name='norecaptcha',
   version='0.2',
   packages=['norecaptcha'],
   description='Python client for the google new No CAPTCHA reCAPTCHA services.',
   long_description=open(README).read(),
   author='Oursky Ltd.',
   author_email='rick.mak@gmail.com',
   url='https://github.com/oursky/norecaptcha',
   download_url='https://www.github.com/oursky/norecaptcha/tarball/master',
   license='MIT',
   classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
