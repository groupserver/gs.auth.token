# coding=utf-8
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()

setup(name='gs.auth.token',
    version=version,
    description="Token authentication for GroupServer",
    long_description=open("README.txt").read() + "\n" +
                    open(os.path.join("docs", "HISTORY.txt")).read(),
    classifiers=[
      "Development Status :: 4 - Beta",
      "Environment :: Web Environment",
      "Framework :: Zope2",
      "Intended Audience :: Developers",
      "License :: Other/Proprietary License",
      "Natural Language :: English",
      "Operating System :: POSIX :: Linux"
      "Programming Language :: Python",
      "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='authentication token database',
    author='Michael JasonSmith',
    author_email='mpj17@onlinegroups.net',
    url='http://groupserver.org',
    license='ZPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['gs', 'gs.auth', ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'gs.option',
        # -*- Extra requirements: -*-
    ],
    entry_points={
        'console_scripts': [
            'gs_auth_token_create = gs.auth.token.createtoken:main',
            ],
        },
)
