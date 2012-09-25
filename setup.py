from setuptools import setup, find_packages
import os

version = '4.1.9'

setup(name='quintagroup.plonecomments',
      version=version,
      description="Plone Comments",
      long_description=open("README.txt").read() + "\n\n" +
          open(os.path.join("docs", "INSTALL.txt")).read() + "\n\n" +
          open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 3.2",
        "Framework :: Plone :: 3.3",
        "Framework :: Plone :: 4.0",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='web zope plone comments discussion',
      author='Quintagroup',
      author_email='support@quintagroup.com',
      url='http://quintagroup.com/services/plone-development'
          '/products/plone-comments',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['quintagroup'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.browserlayer',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      """,
      )
