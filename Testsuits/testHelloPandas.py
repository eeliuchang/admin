#!/usr/bin/env python
import sys
import csv
import hello_pandas
import unittest
import glob
from datetime import datetime
from pandas import DataFrame, Series
import pandas as pd
from pandas.util.testing import assert_frame_equal

class TestHelloDataFunctions(unittest.TestCase):
    currentResult = None


    def setUp(self):
        
        self.columns = ['purchase_price', 'sale_price', 'purchase_q_since_1970', 'sale_q_since_1970']
        self.dir_path = '*.csv'
        self.data_files = glob.glob(self.dir_path)
        self.frames = []
        for f in self.data_files:
            self.new_frame = pd.read_csv(f, names = self.columns)
            self.new_frame['city'] = f.split('/')[-1].split('.')[0]
            self.frames.append(self.new_frame)
        self.frame = pd.concat(self.frames, ignore_index=True)
        self.length = len(self.frame)
        self.purchase_price = self.frame['purchase_price']
        self.city = self.frame['city']

        self.frame_with_year = self.frame.copy()
        self.frame_with_year['sale_q_since_1970_year'] = [((f-1)/4)+1970 for f in self.frame['sale_q_since_1970']]
        self.year = self.frame_with_year['sale_q_since_1970_year']

        self.frame['ownership_duration'] = self.frame['sale_q_since_1970']-self.frame['purchase_q_since_1970']
        self.fast = self.frame[ self.frame['ownership_duration']<4]

        self.fast1 = self.fast.copy()
        self.fast1['profit'] = self.fast1['sale_price']-self.fast1['purchase_price']
        self.mean = self.fast1.profit.mean()

        self.frame_sort = self.frame.copy()
        self.frame_sort['profit'] = self.frame_sort['sale_price']-self.frame_sort['purchase_price']
        self.sort = self.frame_sort.sort_index(by='profit', ascending=False)[:10]
        
        self.counts = pd.value_counts(self.frame['city'], sort=False)


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

    def test_read_all_files(self):
        f_all = hello_pandas.read_all_files('*.csv',self.columns,'city')
        f_length = len(f_all) 
        f_purchse_price = f_all['purchase_price'] 
        self.assertEqual(f_length,self.length) #check the length of data frame
        self.assertEqual(f_purchse_price[1],self.purchase_price[1]) # check the first reading
        self.assertEqual(f_purchse_price[2],self.purchase_price[2]) # check the second reading


    def test_add_source_column(self):
        frames1 = []
        for f1 in self.data_files:
            new_frame1 = pd.read_csv(f1, names = self.columns)
            hello_pandas.add_source_column(new_frame1, 'city', f1)
            frames1.append(new_frame1)
        f = pd.concat(frames1, ignore_index=True)
        f_city = f['city']
        self.assertItemsEqual(f_city,self.city)

    def test_append_year(self):
        #print self.frame[:3]
        sales = self.frame.copy()
        hello_pandas.append_year(sales, 'sale_q_since_1970')    
        self.assertItemsEqual(sales['sale_q_since_1970_year'],self.year)

        #another test for the whole frame

    def test_fast_sales(self):
        sales = self.frame.copy()
        sales_fast = hello_pandas.fast_sales(sales, 4)
        self.assertItemsEqual(sales_fast,self.fast)
        # in some cases, the frame maybe reordered, so 
        #(1) maybe we can sort and take the number 37th row and compare

    def test_profit_on_fast_sales(self):
        sales = self.frame.copy()
        sales_mean = hello_pandas.profit_on_fast_sales(sales,4)
        self.assertTrue(abs(self.mean-sales_mean) < 2)

    def test_most_profitable_sales(self):
        sales = self.frame.copy()
        sales_sort = hello_pandas.most_profitable_sales(sales)
        self.assertItemsEqual(sales_sort['profit'],self.sort['profit'])
        self.assertItemsEqual(sales_sort['city'],self.sort['city'])

    def test_sales_by_city(self):
        sales = self.frame.copy()
        sales_count = hello_pandas.sales_by_city(sales, 'city')
        self.assertItemsEqual(self.counts, sales_count)


if __name__ == '__main__':
    unittest.main()