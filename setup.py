"""Setup access_modifiers."""

import setuptools


setuptools.setup(
    name="access_modifiers",
    version="0.3.1",
    author="Frank Niessink",
    author_email="frank@niessink.com",
    description="Private and protected access modifiers for Python",
    license="Apache 2.0",
    keywords="access modifier,protected,private,oop",
    url="https://github.com/fniessink/access-modifiers",
    packages=setuptools.find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development"])
