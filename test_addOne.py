import hello_data
import unittest


class TestTestDataFunctions(unittest.TestCase):
    currentResult = None

    def setUp(self):
       self.data = 1

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

    def test_test_data(self):
        self.assertEqual(hello_data.test_data(self.data), 2)


if __name__ == '__main__':
    unittest.main()