from setuptools import setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


long_description = read('README.md')

setup(
    name='fuckit',
    version='4.8.1',
    py_modules=['fuckit'],
    url='https://github.com/ajalt/fuckitpy',
    license='WTFPL',
    author='AJ Alt',
    author_email='',
    tests_require=['nose'],
    description='The Python Error Steamroller',
    long_description=long_description,
    platforms='any',
    test_suite='nose.collector',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    extras_require={
        'testing': ['nose'],
    }
)
