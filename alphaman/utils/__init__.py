# MIT License
#
# Copyright (c) 2017 Changsung
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

def daily(start, end):
	return range(start, end+1)
	
def weekly(start, end):
	return map(lambda x: x * 5, range(start, end+1))

def tech_key(data_key, period, tech_ind):
	return str(data_key) + "-" + str(period) + "_" + str(tech_ind)

def calculate_quarter_count(start_date, end_date):
	assert(start_date <= end_date)
	quarter_num = 0
	if start_date.month < 4:
		quarter_num += 4
	elif start_date.month < 5:
		quarter_num += 3
	elif start_date.month < 8:
		quarter_num += 2
	elif start_date.month < 11:
		quarter_num += 1
	else:
		quarter_num += 0

	if end_date.month < 4:
		quarter_num -= 4
	elif end_date.month < 5:
		quarter_num -= 3
	elif end_date.month < 8:
		quarter_num -= 2
	elif end_date.month < 11:
		quarter_num -= 1
	else:
		quarter_num -= 0

	year_delta = end_date.year - start_date.year
	quarter_num += year_delta * 4
	return quarter_num

from datetime import datetime
def quarterify(year, quarter_num):
	""" quarter_num = 1, 2, 3, 4
	"""
	year = int(year)
	assert(quarter_num in [1, 2, 3, 4])
	if quarter_num == 1:
		return datetime(year, 5, 1)
	elif quarter_num == 2:
		return datetime(year, 8, 1)
	elif quarter_num == 3:
		return datetime(year, 11, 1)
	else:
		return datetime(year+1, 4, 1)

def get_closest_quarter(cur_date, past=True):
	if cur_date.month < 4:
		if past:
			return (cur_date.year-1), 3
			#return cur_date.replace(year=(cur_date.year-1), month=11, day=1)
		else:
			return (cur_date.year-1), 4
			#return cur_date.replace(year=(cur_date.year), month=4, day=1)
	elif cur_date.month < 5:
		if past:
			return (cur_date.year-1), 4
			#return cur_date.replace(year=(cur_date.year), month=4, day=1)
		else:
			return (cur_date.year), 1
			#return cur_date.replace(year=(cur_date.year), month=5, day=1)
	elif cur_date.month < 8:
		if past:
			return (cur_date.year), 1
			#return cur_date.replace(year=(cur_date.year), month=5, day=1)
		else:
			return (cur_date.year), 2
			#return cur_date.replace(year=(cur_date.year), month=8, day=1)
	elif cur_date.month < 11:
		if past:
			return (cur_date.year), 2
			#return cur_date.replace(year=(cur_date.year), month=8, day=1)
		else:
			return (cur_date.year), 3
			#return cur_date.replace(year=(cur_date.year), month=11, day=1)
	else:
		if past:
			return (cur_date.year), 3
			#return cur_date.replace(year=(cur_date.year), month=11, day=1)
		else:
			return (cur_date.year), 4
			#return cur_date.replace(year=(cur_date.year+1), month=4, day=1)
