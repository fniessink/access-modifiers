# Access modifiers for Python

[![Build Status](https://travis-ci.com/fniessink/access-modifiers.svg?branch=master)](https://travis-ci.com/fniessink/access-modifiers)
[![PyPI](https://img.shields.io/pypi/v/access-modifiers.svg)](https://pypi.python.org/pypi/access-modifiers)

This package provides two access modifiers for Python: private methods and protected methods. The goal is to be able to document methods as being private or protected and to provide basic guards against accidentally calling private and protected methods from outside the allowed scopes.

## How to use

Example usage of private methods:

```python
from access_modifiers import privatemethod

class Class:
    @privatemethod
    def private_method(self) -> str:
        return "private method"

    def public_method(self) -> str:
        return "public method calls " + self.private_method()

c = Class()
print(c.public_method())  # Prints "public method calls private method"
print(c.private_method())  # Raises an exception
```

Example usage of protected methods:

```python
from access_modifiers import protectedmethod

class Class:
    @protectedmethod
    def protected_method(self) -> str:
        return "protected method"

    def public_method(self) -> str:
        return "public method calls " + self.protected_method()


class Subclass(Class):
    @protectedmethod
    def protected_method(self) -> str:
        return "overridden protected method calls " + super().protected_method()

c = Subclass()
print(c.public_method())  # Prints "public method calls overridden protected method calls protected method"
print(c.protected_method())  # Raises an exception
```

Private methods can be combined with static methods. Note that the order matters: staticmethod should be the outermost decorator.

```python
from access_modifiers import privatemethod

class Class:
    @staticmethod
    @privatemethod
    def static_private_method() -> str:
        return "static private method"

    def public_method(self) -> str:
        return "public method calls " + self.static_private_method()

c = Class()
print(c.public_method())  # Prints "public method calls static private method"
print(c.static_private_method())  # Raises an exception
```

Combining protected methods with static methods is not supported. Combining access modifiers with class methods is not supported (yet).

## Performance

The access modifier decorators work by looking at the code that is calling the decorator to decide whether it is allowed to call the method. To do so, the decorators use implementation details of CPython, like sys._getframe() and the names of code objects such as lambdas and modules. These checks are done on each method call. Consequently, there is a considerable performance impact. Therefore it's recommended to use the access modifiers during testing and turn them off in production using the `access_modifiers.disable()` method. Note that you need to call this method before any of the access modifier decorators are evaluated, i.e.:

```python
from access_modifiers import disable, privatemethod

disable()  # This will disable the access checks

class Class:
    @privatemethod
    def private_method(self) -> str:
        return "private_method"

disable()  # Calling disable here will not work, Class.private_method has already been wrapped
```

## Installation

The package is available from the Python Package Index, install with `pip install access-modifiers`.

## Development 

To clone the repository: `git clone git@github.com:fniessink/access-modifiers.git`.

To install the development dependencies: `pip install -r requirements-dev.txt`.

To run the unittests and measure the coverage (which should always be at 100%): `ci/unittest.sh`.

To run Pylint (which should score a 10) and Mypy (which shouldn't complain): `ci/quality.sh`.

The implementation is driven by (unit) tests and has 100% unit test statement and branch coverage. Please look at the tests to see which usage scenario's are currently covered.
