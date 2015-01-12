#!/usr/bin/env python
import sys
import csv
from datetime import datetime
import hello_data
import unittest
from StringIO import StringIO


class TestHelloDataFunctions(unittest.TestCase):
    currentResult = None


    def setUp(self):
        self.data = 1
        my_file = open("./Sensors.csv", "rU")
        self.readings = list(csv.reader(my_file))
        self.readings_length = len(self.readings)
        self.first_reading = self.readings[1]
        self.last_reading = self.readings[self.readings_length-1]

        self.readings_below_threshold = [self.reading for self.reading in self.readings[1:] if float(self.reading[7])<6]

        self.fullArray_reading_dict = [{'id': reading[9],'battery_life':reading[7]}  for reading in self.readings[1:]]
        self.belowThresholdArray_reading_dic = [{'id': reading[9],'battery_life':reading[7]}  for reading in self.readings_below_threshold]
        
        self.month_num = 8
        self.month_readings = [ reading for reading in self.readings[1:] if datetime.strptime(reading[1], '%m/%d/%y %H:%M').month== self.month_num ] #count number and contents

        self.held, sys.stdout = sys.stdout, StringIO()

    def tearDown(self):
        ok = self.currentResult.wasSuccessful()
        errors = self.currentResult.errors
        failures = self.currentResult.failures
        print ' All tests passed so far!' if ok else \
                ' %d failures so far' % \
                (len(errors) + len(failures))

    def run(self, result=None):
        self.currentResult = result # remember result for use in tearDown
        unittest.TestCase.run(self, result) # call superclass run method

    def test_read_input(self):
        r = hello_data.read_input("./Sensors.csv")
        self.assertEqual(len(r),self.readings_length-1)

    def test_find_low_battery_readings(self):
        r_below = hello_data.find_low_battery_readings(self.readings[1:],6)
        self.assertEqual(r_below, self.readings_below_threshold)

    def test_battery_dict(self):
        r_dict1 = hello_data.battery_dict(self.readings[1:])
        r_dict2 = hello_data.battery_dict(self.readings_below_threshold)
        self.assertEqual(r_dict1,self.fullArray_reading_dict)
        self.assertEqual(r_dict2,self.belowThresholdArray_reading_dic)

    def test_month_readings(self):
        r_m = hello_data.month_readings(self.readings[1:],self.month_num)
        self.assertEqual(r_m,self.month_readings)

    def test_hello_data(self):
        # make sure the printout is exactly "Hello Data!"
        hello_data.hello_data()
        self.assertEqual(sys.stdout.getvalue().strip(), "Hello Data!")



if __name__ == '__main__':
    unittest.main()