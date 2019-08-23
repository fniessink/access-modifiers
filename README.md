# Access modifiers for Python

This package provides two access modifiers for Python: private methods and protected methods.

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
