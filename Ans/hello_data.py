#!/usr/bin/env python
import sys
import csv
from datetime import datetime
# check that datetime is being iumported

def read_input(path) :
	my_file = open(path, "rU")
	readings=list(csv.reader(my_file))
	return readings[1:] # test the length, first and last element of this dataset

def find_low_battery_readings(readings, threshold) :
	return [reading for reading in readings if float(reading[7])<threshold] # count the number and contents of this

def battery_dict(readings) :
	return [{'id': reading[9],'battery_life':reading[7]}  for reading in readings] # test that this works on both the full array of readings and on low_battery

def month_readings(readings, month_num) :
	#make sure using datetime
	return [ reading for reading in readings if datetime.strptime(reading[1], '%m/%d/%y %H:%M').month==month_num ] #count number and contents

def hello_data() :
	print 'Hello Data!' # test that this phrase is printed

print read_input(sys.argv[1])
hello_data()
readings=read_input(sys.argv[1])
print readings[0]
print len(readings)
#low_batt = find_low_battery_readings(readings,6)
#print low_batt[0]
#print battery_dict(low_batt)[0]
#print len(month_readings(readings,8))




#

