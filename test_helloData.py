import hello_data
import unittest
import sys
from StringIO import StringIO

class TestHelloDataFunctions(unittest.TestCase):
    currentResult = None

    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()

    def tearDown(self):
        ok = self.currentResult.wasSuccessful()
        errors = self.currentResult.errors
        failures = self.currentResult.failures
        print ' All tests passed so far!' if ok else \
                ' %d errors and %d failures so far' % \
                (len(errors), len(failures))

    def run(self, result=None):
        self.currentResult = result # remember result for use in tearDown
        unittest.TestCase.run(self, result) # call superclass run method

    def test_hello_data(self):
        # make sure the printout is exactly "Hello Data!"
        hello_data.hello_data()
        self.assertEqual(sys.stdout.getvalue().strip(), "Hello Data!")


if __name__ == '__main__':
    unittest.main()
