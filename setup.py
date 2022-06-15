#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from setuptools import setup, find_packages
from setuptools.command.install import install as InstallCommand
from setuptools.command.test import test as TestCommand

version = "0.1.0rc5"
requirements = "libxml2-dev libxslt-dev python-dev"


class Install(InstallCommand):

    def run(self):
        # params = "{install_params} {requirements}".format(install_params="install", requirements=requirements)
        # cmd = "{command} {params}".format(command="apt-get", params=params)
        # proc = subprocess.Popen(cmd, shell=True)
        # proc.wait()
        InstallCommand.run(self)


class Test(TestCommand):
    user_options = [("pytest-args=", "a", "")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


try:
    long_description = open("README.md", encoding="utf-8").read()
except TypeError:
    long_description = open("README.md").read()

setup(
    name="aiowebdav",
    version=version,
    packages=find_packages(exclude=("tests",)),
    requires=["python (>= 3.8.0)"],
    install_requires=["aiohttp", "lxml", "python-dateutil", "aiofiles"],
    python_requires=">=3.8",
    scripts=["wdc"],
    test_suite="tests",
    tests_require=["pytest"],
    cmdclass={"install": Install, "test": Test},
    description="Asyncio WebDAV client, based on original package https://github.com/ezhov-evgeny/webdav-client-python-3 but "
                "uses aiohttp instead of requests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="synodriver",
    author_email="diguohuangjiajinweijun@gmail.com",
    url="https://github.com/synodriver/aiowebdav",
    license="MIT License",
    keywords="webdav, client, python, module, library, packet, Yandex.Disk, Dropbox, Google Disk, Box, 4shared",
    classifiers=[
        "Environment :: Console",
        "Environment :: Web Environment",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
