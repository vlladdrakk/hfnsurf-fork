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

NUMERALS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def dec_to_base(num, b, numerals = NUMERALS, pad_width = 0):
	
	res = ((num == 0) and numerals[0]) or (dec_to_base(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])
	
	return res.zfill(pad_width)
	
def base_to_dec(s, b, numerals = NUMERALS):
	
	position = len(s)
	res = 0
	
	for dig in s:
		
		position -= 1
		res += numerals.index(dig) * (b ** position)
		
	return res
	
def base_translate(s, base_from, base_to,
					numerals = NUMERALS,
					pad_width=0):
	
	s = str(s)
	dec = base_to_dec(s, base_from, numerals = numerals)
	
	return dec_to_base(dec, base_to, numerals = numerals, pad_width = pad_width)
	
def intlist_base_translate(lst, base_to, base_from = 10,
							numerals = NUMERALS,
							pad_width = 0,
							as_ints = False):
	
	res = []
	
	for num in lst:
		res.append(base_translate(num, base_from, base_to,
								numerals = numerals,
								pad_width = pad_width))
	
	if as_ints and base_to == 10:
		return [int(x) for x in res]
	else:
		return res