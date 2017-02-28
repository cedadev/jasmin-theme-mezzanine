#!/usr/bin/env python3

import os, re

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

try:
    import jasmin_theme_mezzanine.__version__ as version
except ImportError:
    # If we get an import error, find the version string manually
    version = "unknown"
    with open(os.path.join(here, 'jasmin_theme_mezzanine', '__init__.py')) as f:
        for line in f:
            match = re.search('__version__ *= *[\'"](?P<version>.+)[\'"]', line)
            if match:
                version = match.group('version')
                break

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

if __name__ == "__main__":

    setup(
        name = 'jasmin-theme-mezzanine',
        version = version,
        description = 'Django app providing templates for JASMIN Mezzanine websites',
        long_description = README,
        classifiers = [
            "Programming Language :: Python",
            "Framework :: Django",
            "Topic :: Internet :: WWW/HTTP",
            "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
        author = 'Matt Pritchard',
        author_email = 'matt.prithard@stfc.ac.uk',
        url = 'https://github.com/cedadev/jasmin-theme-mezzanine',
        keywords = 'web django jasmin theme bootstrap',
        packages = find_packages(),
        include_package_data = True,
        zip_safe = False,
        install_requires = ['django', 'jasmin-theme-django'],
        extras_require = { 'django-bootstrap3' : ['django-bootstrap3'] },
    )
