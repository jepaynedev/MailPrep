# Placeholder test to make pytest pass and verify tests being found
import unittest

class TestModuleImport(unittest.TestCase):

    def test_import_mailprep(self):
        import mailprep
        self.assertTrue(True)
