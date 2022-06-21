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

CONTROLS = {
	0: 'NUL',
	1: 'SOH',
	2: 'STX',
	3: 'ETX',
	4: 'EOT',
	5: 'ENQ',
	6: 'ACK',
	7: 'BEL',
	8: 'BS',
	9: 'HT',
	10: 'LF',
	11: 'VT',
	12: 'FF',
	13: 'CR',
	14: 'SO',
	15: 'SI',
	16: 'DLE',
	17: 'DC1',
	18: 'DC2',
	19: 'DC3',
	20: 'DC4',
	21: 'NAK',
	22: 'SYN',
	23: 'ETB',
	24: 'CAN',
	25: 'EM',
	26: 'SUB',
	27: 'EDC',
	28: 'FS',
	29: 'GS',
	30: 'RS',
	31: 'US',
	127: 'DEL'
}

def int_to_unicode(num, control_replace = False):
	
	if num in CONTROLS:
		
		if control_replace:
			return '<{}>'.format(CONTROLS[num])
			
		else:
			return '·'
			
	else:
		return chr(num)
	
def int_to_ascii(num, overflow = False, control_replace = False):
	
	if num >= 128:
		
		if overflow:
			num = num%128
			
		elif control_replace:
			return '·'
			
		else:
			return '<?>'
	
	return int_to_unicode(num)

def intlist_to_unicode(lst, delim = None, control_replace = False):
	
	res = []
	
	for num in lst:
		res.append(int_to_unicode(num, control_replace = control_replace))
			
	if delim is not None:
		return delim.join(res)
	else:
		return res
		
def intlist_to_ascii(lst, delim = None, overflow = False, control_replace = False):
		
	res = []
	
	for num in lst:
		res.append(int_to_ascii(num, overflow = overflow, control_replace = control_replace))
			
	if delim is not None:
		return delim.join(res)
	else:
		return res