# Access modifiers for Python

[![Build Status](https://travis-ci.org/fniessink/access-modifiers.svg?branch=master)](https://travis-ci.org/fniessink/access-modifiers)

This package provides two access modifiers for Python: private methods and protected methods.

## Example usage

Example usage of private methods:

```python
from access_modifiers import privatemethod

class Class:
    @privatemethod
    def private_method(self) -> str:
        """A private method."""
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
        """A protected method."""
        return "protected method"

    def public_method(self) -> str:
        return "public method calls " + self.protected_method()


class Subclass(Class):
    @protectedmethod
    def protected_method(self) -> str:
        """An overridden protected method."""
        return "overridden protected method calls " + super().protected_method()

c = Subclass()
print(c.public_method())  # Prints "public method calls overridden protected method calls protected method"
print(c.protected_method())  # Raises an exception
```

## Installation

There is no release to the Python Package Index yet, so you'll have to install from source. Clone the repository and run `python setup.py install`.

## Tests and quality

To install the development dependencies: `pip install -r requirements-dev.txt`.

To run the unittests and measure the coverage (which should always be at 100%): `ci/unittest.sh`.

To run Pylint (which should score a 10) and Mypy (which shouldn't complain): `ci/quality.sh`.

## Implementation notes

Both the `privatemethod` and the `protectedmethod` decorator work by looking at the code that is calling the decorator using the inspect module to decide whether it is allowed to call the method. Look at the tests to see which scenario's are currently covered.

Unsupported/untested are nested decorators, e.g.: 

```python
class Class:
    @privatemethod
    @staticmethod
    def private_static_method():
        return "a private static method"  # This is unsupported and untested!
```
