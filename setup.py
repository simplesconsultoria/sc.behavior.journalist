# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import os

version = '1.0a2.dev0'
description = "Adds Journalist especific information to the Person content \
type defined in s17.person.",
long_description = open("README.rst").read() + "\n" + \
    open(os.path.join("docs", "INSTALL.rst")).read() + "\n" + \
    open(os.path.join("docs", "CREDITS.rst")).read() + "\n" + \
    open(os.path.join("docs", "HISTORY.rst")).read()

setup(
    name='sc.behavior.journalist',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Office/Business :: News/Diary",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='plone dexterity behaviors journalism news',
    author='Simples Consultoria',
    author_email='products@simplesconsultoria.com.br',
    url='https://github.com/simplesconsultoria/sc.behavior.journalist',
    license='GPLv2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['sc', 'sc.behavior'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Pillow',
        'plone.behavior',
        'plone.directives.form',
        'Products.CMFDefault',
        'Products.GenericSetup',
        's17.person',
        'setuptools',
        'zope.component',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.dexterity',
            'plone.testing',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
