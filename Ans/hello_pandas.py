#!/usr/bin/env python
import sys
import csv
import glob
from datetime import datetime
from pandas import DataFrame, Series
import pandas as pd


#read multiple files into one frame
# TEST:  check number of rows in dataframe
# and check row contents for a few
# and check indexes
def read_all_files(dir_path, columns, source_column) :
	data_files = glob.glob(dir_path)
	frames = []
	for f in data_files:
		new_frame = pd.read_csv(f, names = columns)
		add_source_column(new_frame, source_column, f)
		frames.append(new_frame)
	return pd.concat(frames, ignore_index=True)

#TEST:  a unit test for this function.
def add_source_column(frame, col_name, file_source):
	frame[col_name] = file_source.split('/')[-1].split('.')[0]

#TEST:  check this works.  check input column type
def append_year(frame, col) :
	frame[col+'_year'] = [((f-1)/4)+1970 for f in frame[col]]

# TEST:  check that the number of records is correct
# and spot check a few records
def fast_sales(frame, period) :
	frame['ownership_duration'] = frame['sale_q_since_1970']-frame['purchase_q_since_1970']
	return frame[ frame['ownership_duration']<period ]

# TEST the value of the mean computed (within some tolerance)
def profit_on_fast_sales(frame, period) :
	new_frame = fast_sales(frame, period).copy()
	new_frame['profit'] = new_frame['sale_price']-new_frame['purchase_price']
	return new_frame.profit.mean()

#  TEST all 10 values
def most_profitable_sales(frame) :
	frame['profit'] = frame['sale_price']-frame['purchase_price']
	return frame.sort_index(by='profit', ascending=False)[:10]

# TEST  all 4 values
def sales_by_city(frame, col_name) :
	return pd.value_counts(frame[col_name], sort=False)

columns = ['purchase_price', 'sale_price', 'purchase_q_since_1970', 'sale_q_since_1970']
sales = read_all_files('*.csv', columns, 'city')
append_year(sales, 'sale_q_since_1970')
#print sales[:3]
print len(fast_sales(sales, 4))
#print profit_on_fast_sales(sales,4)
#print sales_by_city(sales, 'city')
print most_profitable_sales(sales)
