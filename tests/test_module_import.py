# Placeholder test to make pytest pass and verify tests being found
import unittest

class TestModuleImport(unittest.TestCase):

    def test_import_mailprep(self):
        """Simply tries to import mailprep module then assert True. If import fails then exception will be thrown and test will fail."""
        import mailprep
        self.assertTrue(True)
