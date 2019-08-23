"""Unit tests for the private method access modifier."""

import unittest

from ..access_modifiers import AccessException, privatemethod, protectedmethod


class PrivateMethodTest(unittest.TestCase):
    """Unit tests for the @privatemethod decorator."""

    # pylint: disable=missing-docstring

    class Class:
        @privatemethod
        def private_method(self):  # pylint: disable=no-self-use
            return "Class.private_method"

        def public_method(self):
            return "Class.public_method -> " + self.private_method()

    def test_call_private_method_directly(self):
        """Test the accessing a private method throws an exception."""
        self.assertRaises(AccessException, self.Class().private_method)
        self.assertRaises(AccessException, self.Class.private_method, self.Class())

    def test_call_private_method_via_public_method(self):
        """Test the accessing a private method via a public method is allowed."""
        self.assertEqual("Class.public_method -> Class.private_method", self.Class().public_method())

    def test_call_private_method_via_public_method_from_subclass(self):
        """Test the accessing a private method via an overridden public method is allowed."""

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
        """Test the accessing a private method via a public method in a subclass is not allowed,
        not even when using super()."""

        class Subclass(self.Class):
            def public_method(self):
                super().private_method()

        self.assertRaises(AccessException, Subclass().public_method)

    def test_override_private_method(self):
        """Test that an overridden private method can't call its super."""

        class Subclass(self.Class):
            @privatemethod
            def private_method(self):
                super().private_method()  # pragma: nocover

        self.assertRaises(AccessException, Subclass().public_method)

    def test_override_private_method_with_protected_method(self):
        """Test that a private method cannot be overridden with a protected method."""

        class Subclass(self.Class):
            @protectedmethod
            def private_method(self):
                return "Subclass.private_method -> " + super().private_method()

        self.assertEqual("Class.public_method -> Class.private_method", self.Class().public_method())
        self.assertRaises(AccessException, Subclass().public_method)
        self.assertRaises(AccessException, Subclass().private_method)
