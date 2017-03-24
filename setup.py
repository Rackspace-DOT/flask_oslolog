# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Flask-OsloLog adds logging via oslo.log to Flask.

No configuration is necessary for this extension outside of the standard
`oslo.log` configuration done via `oslo.config`. This extension will by
default use the following format:

'%(REMOTE_ADDR)s %(REMOTE_USER)s %(REMOTE_STATUS)s '
              '"%(REQUEST_METHOD)s %(REQUEST_URI)s" status: %(status)s'
              ' len: %(bytes)s'

Example:
2017-01-19 18:30:26.654 2082 INFO flask_oslolog.middleware [-] 10.19.26.194 \
 russ7612 Confirmed "GET /v1/prefab/1" status: 200 len: 8317

    REMOTE_ADDR:   Standard remote_addr header.
    REMOTE_USER:   If using keystone middleware, this will map to X-User-Id
    REMOTE_STATUS: If using keystone middleware, this will map to
                   X-Identity-Status
    REMOTE_METHOD: REST method (GET/PUT/POST/DELETE, etc.)
    REQUEST_URI:   endpoint uri, including query string.
    status:        response status code.
    len:           response byte length.
"""

import io
import re
import ast
import sys

from os import path

from setuptools import find_packages, setup
from setuptools.command.test import test

here = path.abspath(path.dirname(__file__))

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('flask_oslolog/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


class Tox(test):
    """
    TestCommand to run ``tox`` via setup.py.
    Allows running of tox tests via `python setup.py test`.
    """

    def finalize_options(self):
        """
        Finalize options from args.
        Standard Tox args can be passed to `setup.py` test
        as if it were the tox executable.
        """
        test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        """
        Pass test running off to the Tox `cmdline` construct.
        args can be passed in on the command line as they would to
        the standard Tox executable, like so:
        .. code-block:: bash
            python setup.py test --version
        """
        # import here, cause outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)


def read(*filenames, **kwargs):
    """
    Read file contents into string.
    Used by setup.py to concatenate long_description.
    :param string filenames: Files to be read and concatenated.
    :rtype: string
    """
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        if path.splitext(filename)[1] == ".md":
            try:
                import pypandoc
                buf.append(pypandoc.convert_file(filename, 'rst'))
                continue
            except:
                with io.open(filename, encoding=encoding) as f:
                    buf.append(f.read())
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


setup(
    name='flask_oslolog',
    version=version,
    description=(
        'This project wraps the existing oslo.log library to provide'
        'request logging and logger access within flask..'
    ),
    long_description=read("README.md"),

    # The project's main homepage.
    url='https://github.com/Rackspace-DOT/flask_oslolog',

    # Author details
    author='Rackspace Developers for Operational Tooling',
    author_email='dot@rackspace.com',
    platforms="any",
    install_requires=[
        'Flask',
        'oslo.config',
        'oslo.log',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',

        'Intended Audience :: Developers',

        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
        'Topic :: Software Development :: Libraries :: Python Modules'

        'License :: OSI Approved :: Apache Software License',

        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],

    keywords=['flask', 'identity', 'auth'],
    tests_require=['tox', 'virtualenv'],
    cmdclass={'test': Tox},

    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    entry_points={
        'console_scripts': [],
    }
)
