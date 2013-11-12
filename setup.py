#!/usr/bin/env python
# Copyright [2013] [Kevin Carter]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import setuptools
import sys

from mungerator import info

REQUIRES = ['PyChef==0.2.2']

if sys.version_info < (2, 6, 0):
    sys.stderr.write("The Mungerator requires Python 2.6.0 or greater \n")
    raise SystemExit(
        '\nUpgrade python because you version of it is VERY deprecated\n'
    )
elif sys.version_info < (2, 7, 0):
    REQUIRES.append('argparse')

with open('README', 'rb') as r_file:
    LDINFO = r_file.read()

setuptools.setup(
    name=info.__appname__,
    version=info.__version__,
    author=info.__author__,
    author_email=info.__email__,
    description=info.__description__,
    long_description=LDINFO,
    license=info.__license__,
    packages=['mungerator',
              'mungerator.arguments',
              'mungerator.methods'],
    url=info.__url__,
    install_requires=REQUIRES,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    entry_points={
        "console_scripts": ["mungerator = mungerator.executable:execute"]}
)
