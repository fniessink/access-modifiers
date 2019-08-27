"""Unit tests for the private method access modifier."""

import unittest

from ..access_modifiers import AccessException, disable, enable, privatemethod, protectedmethod


class PrivateMethodTests(unittest.TestCase):
    """Shared unit tests for the private method and static private method access modifiers."""

    # pylint: disable=missing-docstring,too-few-public-methods

    class Class:
        @privatemethod
        def private_method(self):  # pylint: disable=no-self-use
            return "Class.private_method"

        @privatemethod
        def private_method_calling_private_method(self):
            return "Class.private_method_calling_private_method -> " + self.private_method()

        def public_method(self):
            return "Class.public_method -> " + self.private_method()

        def public_method_calling_private_method_via_private_method(self):
            return "Class.public_method_calling_private_method_via_private_method -> " + \
                   self.private_method_calling_private_method()

        def public_method_using_list_comprehension(self):
            return ["Class.public_method -> " + self.private_method() for _ in range(1)][0]

        def public_method_using_nested_lambdas(self):
            # pylint: disable=unnecessary-lambda
            inner_lambda_function = lambda: self.private_method()
            outer_lambda_function = lambda: "Class.public_method -> " + inner_lambda_function()
            return outer_lambda_function()

        def public_method_using_try_except(self):
            try:
                return "Class.public_method -> " + self.private_method()
            except AttributeError:  # pragma: nocover
                pass

    class Subclass(Class):
        @privatemethod
        def private_method(self):
            super().private_method()  # pragma: nocover

    class SubclassOverridesWithProtectedMethod(Class):
        @protectedmethod
        def private_method(self):
            return "Subclass.private_method -> " + super().private_method()  # pragma: nocover

    def test_call_private_method_directly(self):
        """Test that accessing a private method throws an exception."""
        self.assertRaises(AccessException, self.Class().private_method)

    def test_call_private_method_directly_without_access_checks(self):
        """Test that accessing a private method without access checks works."""
        try:
            disable()

            class Class:
                @privatemethod
                def private_method(self):  # pylint: disable=no-self-use
                    return "Class.private_method"

            self.assertEqual("Class.private_method", Class().private_method())
        finally:
            enable()

    def test_call_private_method_via_public_method(self):
        """Test that accessing a private method via a public method is allowed."""
        self.assertEqual("Class.public_method -> Class.private_method", self.Class().public_method())

    def test_call_private_method_via_public_method_from_subclass(self):
        """Test that accessing a private method via an overridden public method is allowed."""

        class Subclass(self.Class):
            def public_method(self):
                return "Subclass.public_method -> " + super().public_method()

        self.assertEqual(
            "Subclass.public_method -> Class.public_method -> Class.private_method", Subclass().public_method())

    def test_call_private_method_via_public_method_in_subclass(self):
        """Test that accessing a private method via a public method in a subclass is not allowed."""

        class Subclass(self.Class):
            def public_method(self):
                self.private_method()

        self.assertRaises(AccessException, Subclass().public_method)

    def test_call_private_method_via_public_method_in_subclass_using_super(self):
        """Test that accessing a private method via a public method in a subclass is not allowed,
        not even when using super()."""

        class Subclass(self.Class):
            def public_method(self):
                super().private_method()

        self.assertRaises(AccessException, Subclass().public_method)

    def test_call_private_method_via_list_comprehension(self):
        """Test that accessing a private method via a list comprehension in a public method works."""
        self.assertEqual(
            "Class.public_method -> Class.private_method", self.Class().public_method_using_list_comprehension())

    def test_call_private_method_via_nested_lambda(self):
        """Test that accessing a private method via a nested lambda in a public method works."""
        self.assertEqual(
            "Class.public_method -> Class.private_method", self.Class().public_method_using_nested_lambdas())

    def test_call_private_method_from_try_except_block(self):
        """Test that accessing a private method from a try/except in a public method works."""
        self.assertEqual("Class.public_method -> Class.private_method", self.Class().public_method_using_try_except())

    def test_override_private_method(self):
        """Test that an overridden private method can't call its super."""
        self.assertRaises(AccessException, self.Subclass().public_method)

    def test_override_private_method_with_protected_method(self):
        """Test that a private method cannot be overridden with a protected method."""
        self.assertEqual("Class.public_method -> Class.private_method", self.Class().public_method())
        self.assertRaises(AccessException, self.Subclass().public_method)
        self.assertRaises(AccessException, self.Subclass().private_method)

    def test_call_private_method_via_private_method(self):
        """Test that a private method can be called via another private method."""
        self.assertEqual(
            "Class.public_method_calling_private_method_via_private_method -> "
            "Class.private_method_calling_private_method -> Class.private_method",
            self.Class().public_method_calling_private_method_via_private_method())


class StaticPrivateMethodTests(PrivateMethodTests):
    """Unit tests for the combined @staticmethod @privatemethod decorator."""

    # pylint: disable=missing-docstring

    class Class:
        @staticmethod
        @privatemethod
        def private_method():
            return "Class.private_method"

        @privatemethod
        def private_method_calling_private_method(self):
            return "Class.private_method_calling_private_method -> " + self.private_method()

        def public_method(self):
            return "Class.public_method -> " + self.private_method()

        def public_method_calling_private_method_via_private_method(self):
            return "Class.public_method_calling_private_method_via_private_method -> " + \
                   self.private_method_calling_private_method()

        def public_method_using_list_comprehension(self):
            return ["Class.public_method -> " + self.private_method() for _ in range(1)][0]

        def public_method_using_nested_lambdas(self):
            # pylint: disable=unnecessary-lambda
            inner_lambda_function = lambda: self.private_method()
            outer_lambda_function = lambda: "Class.public_method -> " + inner_lambda_function()
            return outer_lambda_function()

        def public_method_using_try_except(self):
            try:
                return "Class.public_method -> " + self.private_method()
            except AttributeError:  # pragma: nocover
                pass

    class Subclass(Class):
        @staticmethod
        @privatemethod
        def private_method():
            super().private_method()  # pragma: nocover

    class SubclassOverridesWithProtectedMethod(Class):
        @protectedmethod
        def private_method(self):
            return "Subclass.private_method -> " + super().private_method()  # pragma: nocover

    def test_call_private_method_directly_without_access_checks(self):
        """Test that accessing a private method without access checks works."""
        try:
            disable()

            class Class:  # pylint: disable=too-few-public-methods
                @staticmethod
                @privatemethod
                def private_method():
                    return "Class.private_method"

            self.assertEqual("Class.private_method", Class().private_method())
        finally:
            enable()
