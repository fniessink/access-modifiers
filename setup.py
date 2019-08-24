"""Setup access_modifiers."""

from setuptools import setup


setup(
    name="access_modifiers",
    version="0.1.0",
    author="Frank Niessink",
    author_email="frank@niessink.com",
    description="Private and protected access modifiers for Python",
    license="Apache 2.0",
    keywords="access modifier,protected,private,oop",
    url="https://github.com/fniessink/access_modifiers",
    packages=['access_modifiers'],
    long_description=open('README.md').read(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6"
        "Programming Language :: Python :: 3.7"
        "Programming Language :: Python :: 3.8"
        "Topic :: Software Development"])
