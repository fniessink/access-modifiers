"""Access modifiers for Python."""

from functools import wraps
from sys import _getframe as getframe
from typing import Callable, TypeVar


class AccessException(Exception):
    """Exception raised when a private or protected method is called from outside the class."""


ReturnType = TypeVar('ReturnType')


def privatemethod(method: Callable[..., ReturnType]) -> Callable[..., ReturnType]:
    """Decorator that creates a private method."""
    method_class_qualname = getframe(1).f_locals.get("__qualname__")
    @wraps(method)
    def private_method_wrapper(*args, **kwargs) -> ReturnType:
        """Wrap the original method to make it private."""
        caller_frame = getframe(1)
        caller_code = caller_frame.f_code
        caller_name = caller_code.co_name
        while caller_name.startswith("<") and caller_frame.f_back:
            # Code is a <lambda>, <dictcomp>, <listcomp>, or other non-method code block
            caller_frame = caller_frame.f_back
            caller_code = caller_frame.f_code
            caller_name = caller_code.co_name
        caller_class = caller_frame.f_locals.get("self").__class__
        # Look up the caller method to see if it's defined in the same class as the wrapped method
        classes = [cls for cls in caller_class.mro() if caller_name in cls.__dict__]
        for cls in classes:
            caller = cls.__dict__[caller_name]
            caller = caller.__dict__["__wrapped__"] if "__wrapped__" in caller.__dict__ else caller
            if caller.__code__ == caller_code and method_class_qualname == cls.__qualname__:
                return method(*args, **kwargs)
        raise AccessException(f"Attempted call to private method {method} from outside its class")
    return private_method_wrapper


def protectedmethod(method: Callable[..., ReturnType]) -> Callable[..., ReturnType]:
    """Decorator that creates a protected method."""
    @wraps(method)
    def protected_method_wrapper(*args, **kwargs) -> ReturnType:
        """Wrap the original method to make it protected."""
        caller_frame = getframe(1)
        caller_instance = caller_frame.f_locals.get("self")
        if caller_instance is not args[0]:
            raise AccessException(f"Attempted call to protected method {method} from another object")
        return method(*args, **kwargs)
    return protected_method_wrapper
