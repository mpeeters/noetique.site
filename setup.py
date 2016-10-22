# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = '5.0'

setup(
    name='noetique.site',
    version=version,
    description="",
    long_description=open("README.rst").read(),
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    author='Sébastien Verbois',
    author_email='sebastien.verbois@gmail.com',
    url='https://github.com/sverbois/noetique.site',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['noetique'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.api',
        'plone.app.dexterity',
        'setuptools',
        'z3c.jbot',
    ],
    entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
