"""Performance tests for the access modifiers."""

import timeit
import unittest


class PerformanceTest(unittest.TestCase):
    """Performance tests for the access modifiers."""

    def setUp(self):
        self.number = 10_000  # How often to repeat the performance test with timeit.

    def test_create_private_method(self):
        """Test the time it takes to create private methods as compared to methods without access modifier."""
        time_without_modifier = timeit.timeit("""
class C:
    def private_method(self):
        pass
""", setup="from access_modifiers import privatemethod", number=self.number)

        time_with_modifier = timeit.timeit("""
class C:
    @privatemethod
    def private_method(self):
        pass
""", setup="from access_modifiers import privatemethod", number=self.number)
        self.assertLess(time_with_modifier, time_without_modifier * 3)

    def test_create_protected_method(self):
        """Test the time it takes to create protected methods as compared to methods without access modifier."""
        time_without_modifier = timeit.timeit("""
class C:
    def public_method(self):
        pass
""", setup="from access_modifiers import protectedmethod", number=self.number)

        time_with_modifier = timeit.timeit("""
class C:
    @protectedmethod
    def protected_method(self):
        pass
""", setup="from access_modifiers import protectedmethod", number=self.number)
        self.assertLess(time_with_modifier, time_without_modifier * 3)

    def test_call_private_method(self):
        """Test the time it takes to call private methods as compared to methods without access modifier."""
        time_without_modifier = timeit.timeit("c.public_method()", setup="""
from access_modifiers import privatemethod
class C:
    def private_method(self):
        pass
    def public_method(self):
        self.private_method()
c = C()
""", number=self.number)

        time_with_modifier = timeit.timeit("c.public_method()", setup="""
from access_modifiers import privatemethod
class C:
    @privatemethod
    def private_method(self):
        pass
    def public_method(self):
        self.private_method()
c = C()
""", number=self.number)
        self.assertLess(time_with_modifier, time_without_modifier * 15)

    def test_call_protected_method(self):
        """Test the time it takes to call protected methods as compared to methods without access modifier."""
        time_without_modifier = timeit.timeit("c.public_method()", setup="""
from access_modifiers import protectedmethod
class C:
    def protected_method(self):
        pass
    def public_method(self):
        self.protected_method()
c = C()
""", number=self.number)

        time_with_modifier = timeit.timeit("c.public_method()", setup="""
from access_modifiers import protectedmethod
class C:
    @protectedmethod
    def protected_method(self):
        pass
    def public_method(self):
        self.protected_method()
c = C()
""", number=self.number)
        self.assertLess(time_with_modifier, time_without_modifier * 10)
