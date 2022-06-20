# Copyright © 2022 Keith Aprilnight
# This file is part of muodata.
# 
# muodata is free software: you can redistribute it and/or modify it under 
# the terms of the GNU General Public License as published by the Free 
# Software Foundation, either version 3 of the License, or (at your option) 
# any later version.
# 
# muodata is distributed in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for 
# more details.
# 
# You should have received a copy of the GNU General Public License along 
# with muodata. If not, see <https://www.gnu.org/licenses/>. 

###############################################################################

from datetime import date, datetime, timedelta
from .binary import *

###############################################################################


DAYS_OF_WEEK = ['mon','tue','wed','thu','fri','sat','sun']
MONTHS =  ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']


def datetime_from_shortrep(dtstr, notime = False):
	
	dtcls = date if notime else datetime
	
	oneday = timedelta(days=1)
	
	if notime:
		dt = date.today()

	else:	
		
		dt = datetime.now()	
		hour = 0
		minute = 0
	
	day = dt.day
	month = dt.month
	year = dt.year
		
	if dtstr == 'now':
		return dt
		
	elif dtstr in ('today', 'td'):
		return dtcls(year,month,day)
		
	elif dtstr in ('tm', 'tom', 'tomorrow'):
		return dtcls(year,month,day) + oneday
		
	elif dtstr in ('datm', 'ttm'):
		return dtcls(year,month,day) + oneday + oneday
		
	elif dtstr in ('yesterday', 'yest', 'yes', 'ys'):
		return dtcls(year,month,day) - oneday
		
	elif dtstr in ('nextweek', 'nw'):
		return dtcls(year,month,day) + timedelta(days=7)
		
	elif dtstr in ('nm', 'nextmonth'):
		nextmonth = ((month%12) + 1)
		return dtcls(year,nextmonth,day)
	
	dtstr = dtstr.split(' ')
	
	if dtstr:
		
		day = int(dtstr[0])
		
		if len(dtstr) > 1:
			
			if dtstr[1] in MONTHS:
				month = MONTHS.index(dtstr[1])+1
				
			else:
				month = int(dtstr[1])
		
		if len(dtstr) > 2:
			
			year = int(dtstr[2])
			
			if year<2000:
				year = 2000+year
		
		if not notime:
			if len(dtstr) > 3:
				hour = int(dtstr[3])
			
			if len(dtstr) > 4:
				minute = int(dtstr[4])
			
		if notime:
			dt = date(year,month,day)
		else:
			dt = datetime(year,month,day,hour=hour,minute=minute)
		
		return dt
	
	
def date_from_shortrep(dtstr):
	return datetime_from_shortrep(dtstr, notime = True)
	

def date_shortrep(dt, seconds = False):

	mn = MONTHS[dt.month-1]	
	res = f'{dt.day} {mn}'
	
	if dt.year != datetime.now().year:
		res += f' {str(dt.year)[-2:]}'
	
	if isinstance(dt, datetime):
		if dt.hour>0 and dt.minute>0:
			if seconds:
				res += f' {str(dt.hour).zfill(2)}:{str(dt.minute).zfill(2)}:{str(dt.second).zfill(2)}'
			else:
				res += f' {str(dt.hour).zfill(2)}:{str(dt.minute).zfill(2)}'
		
	return res
	
	
def date_to_4_bytes(dt):
	
	res = []
	res.append(unsigned_int_to_bytes(dt.year, bytelen=2))
	res.append(unsigned_int_to_bytes(dt.month, bytelen=1))
	res.append(unsigned_int_to_bytes(dt.day, bytelen=1))
	
	return b''.join(res)
	
	
def date_from_4_bytes(b):
	
	year = bytes_to_unsigned_int(b[0:2])
	month = bytes_to_unsigned_int(b[2:3])
	day = bytes_to_unsigned_int(b[3:4])
	
	return date(year,month,day)
	
	
def datetime_to_7_bytes(dt):
	
	res = []
	res.append(unsigned_int_to_bytes(dt.year, bytelen=2))
	res.append(unsigned_int_to_bytes(dt.month, bytelen=1))
	res.append(unsigned_int_to_bytes(dt.day, bytelen=1))
	res.append(unsigned_int_to_bytes(dt.hour, bytelen=1))
	res.append(unsigned_int_to_bytes(dt.minute, bytelen=1))
	res.append(unsigned_int_to_bytes(dt.second, bytelen=1))
	
	return b''.join(res)
	
	
def datetime_from_7_bytes(b):
	
	year = bytes_to_unsigned_int(b[0:2])
	month = bytes_to_unsigned_int(b[2:3])
	day = bytes_to_unsigned_int(b[3:4])
	hour = bytes_to_unsigned_int(b[4:5])
	minute = bytes_to_unsigned_int(b[5:6])
	second = bytes_to_unsigned_int(b[6:7])
	
	return datetime(year,month,day,hour=hour,minute=minute,second=second)