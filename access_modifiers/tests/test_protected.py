"""Unit tests for the protected method access modifier."""

import unittest

from ..access_modifiers import AccessException, protectedmethod, privatemethod


class ProtectedMethodTest(unittest.TestCase):
    """Unit tests for the @protectedmethod decorator."""

    # pylint: disable=missing-docstring

    class Class:
        @protectedmethod
        def protected_method(self):  # pylint: disable=no-self-use
            return "Class.protected_method"

        def public_method(self):
            return "Class.public_method -> " + self.protected_method()

    def test_protected_method(self):
        """Test that accessing a protected method throws an exception."""
        self.assertRaises(AccessException, self.Class().protected_method)
        self.assertRaises(AccessException, self.Class.protected_method, self.Class())

    def test_call_protected_method_via_public_method(self):
        """Test the accessing a protected method via a public method is allowed."""
        self.assertEqual("Class.public_method -> Class.protected_method", self.Class().public_method())

    def test_call_protected_method_via_protected_method(self):
        """Test the accessing a protected method via a another protected method is allowed."""

        class Subclass(self.Class):
            @protectedmethod
            def another_protected_method(self):
                return "Subclass.another_protected_method -> " + self.protected_method()

            def another_public_method(self):
                return "Subclass.another_public_method -> " + self.another_protected_method()

        self.assertEqual(
            "Subclass.another_public_method -> Subclass.another_protected_method -> Class.protected_method",
            Subclass().another_public_method())

    def test_call_protected_method_via_public_method_in_subclass(self):
        """Test that accessing a protected method via a public method in a subclass is allowed."""

        class Subclass(self.Class):
            def public_method(self):
                return "Subclass.public_method -> " + self.protected_method()

        self.assertEqual("Subclass.public_method -> Class.protected_method", Subclass().public_method())

    def test_call_protected_method_via_overridden_public_method(self):
        """Test that accessing a protected method via an overridden public method in a subclass is allowed."""

        class Subclass(self.Class):
            def public_method(self):
                return "Subclass.public_method -> " + super().public_method()

        self.assertEqual(
            "Subclass.public_method -> Class.public_method -> Class.protected_method", Subclass().public_method())

    def test_call_protected_method_via_public_method_using_super(self):
        """Test that accessing a protected method via a public method in a subclass is allowed,
        also when using super()."""

        class Subclass(self.Class):
            def public_method(self):
                return "Subclass.public_method -> " + super().protected_method()

        self.assertEqual("Subclass.public_method -> Class.protected_method", Subclass().public_method())

    def test_call_overridden_protected_method_via_overridden_public_method(self):
        """Test that a protected method can be overridden."""

        class Subclass(self.Class):
            @protectedmethod
            def protected_method(self):
                return "Subclass.protected_method -> " + super().protected_method()

            def public_method(self):
                return "Subclass.public_method -> " + super().public_method()

        self.assertEqual(
            "Subclass.public_method -> Class.public_method -> Subclass.protected_method -> Class.protected_method",
            Subclass().public_method())

    def test_override_protected_method_with_protected_method(self):
        """Test that a protected method can be overridden with a protected method."""

        class Subclass(self.Class):
            @protectedmethod
            def protected_method(self):
                return "Subclass.protected_method -> " + super().protected_method()

        self.assertEqual(
            "Class.public_method -> Subclass.protected_method -> Class.protected_method", Subclass().public_method())

    def test_override_protected_method_with_public_method(self):
        """Test that a protected method can be overridden with a public method."""

        class Subclass(self.Class):
            def protected_method(self):
                return "Subclass.protected_method -> " + super().protected_method()

        self.assertEqual(
            "Class.public_method -> Subclass.protected_method -> Class.protected_method", Subclass().public_method())
        self.assertEqual("Subclass.protected_method -> Class.protected_method", Subclass().protected_method())

    def test_override_protected_method_with_private_method(self):
        """Test that a protected method cannot be overridden with a private method."""

        class Subclass(self.Class):
            @privatemethod
            def protected_method(self):
                return "Subclass.protected_method -> " + super().protected_method()  # pragma: nocover

        self.assertEqual("Class.public_method -> Class.protected_method", self.Class().public_method())
        self.assertRaises(AccessException, Subclass().public_method)
        self.assertRaises(AccessException, Subclass().protected_method)
