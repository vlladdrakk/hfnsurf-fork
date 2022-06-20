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

from typing import Any, Union

from .bases import *
from .ascii import *

###############################################################################

def list_to_pairs(lst: list) -> list:
	"""Transform a list like [0,1,2,3] into a list of pairs
	[0,1],[1,2],[2,3]
	"""

	if lst:
		return [(lst[i], lst[i+1]) for i in range(0,len(lst)-1)]
	else:
		return []

def center_string(s: str, i: int) -> str:

	l = i - len(s)
	return ' '*int(l/2.0)+s

def c_justify(s: str, i: int) -> str:

	s = shrink_string_end(s, i)
	
	l = i - len(s)
	leftpad = int(l/2.0)
	rightpad = l - leftpad
	
	return f"{' '*leftpad}{s}{' '*rightpad}"
	
def r_justify(s: str, i: int) -> str:

	s = shrink_string_end(s, i)
	
	l = i - len(s)
	
	return f"{' '*l}{s}"
	
	
def l_justify(s: str, i: int) -> str:

	s = shrink_string_end(s, i)
	
	l = i - len(s)
	
	return f"{s}{' '*l}"
	
cj = c_justify
rj = r_justify
lj = l_justify
	
def shrink_string(s: str, i: int) -> str:
	
	
	if (len(s)<7) or (len(s)<=i):
		return s
		
	else:
		
		return s[0:2]+'..'+s[-i+4:]

def bytestring_split_by_two(s, leftfill= '0'):
	
	res = []
	
	if len(s)%2>0:
		s = leftfill+s
	
	while s:
		res.append(s[:2])
		s = s[2:]
	
	return res
	
def shrink_string_end(s: str, i: int) -> str:
	"""
	Shortens string s to a string ending with
	two periods, with length i
	"""
	
	s = str(s)
	
	if len(s) <= i:
		return s
	
	else:
		return s[:i]+'..'
		
def byte_hex_shorthand(b: bytes) -> str:
	"""
	Represent long bytes sequences as neat hex 
	shorthands enclosed in triangle brackets
	"""

	try:
		
		full = b.hex()

		if len(full)>12:
			return '<<'+full[0:6]+'..'+full[-6:]+'>>'
		
		else:
			return '<<'+full+'>>'
	
	except:
		return '<<??????..??????>>'

		
def list_as_table(lst, cols = 4):
	
	res = []
	
	col = 0
	ln = []
	
	for num in lst:
		ln.append(num)
		col += 1
		
		if col>= cols:
			
			col=0		
			res.append('\t'.join(ln))
			ln = []
			
	return('\n'.join(res))
				
def intlist_decdump(src_lst, cols = 8):
	
	lst = src_lst[::]
	res = [f'- - - -\ndecdump: {len(lst)} bytes']

	colcount = 0
	decs = []
	chars = []
	
	while len(lst)>0:
		
		bt = lst.pop(0)
			
		dec = str(bt).rjust(3)
		ch = int_to_ascii(bt, control_replace = True)
			
		decs.append(dec)
		chars.append(ch)
				
		colcount += 1
		
		if (colcount == cols) or (len(lst)==0):
			colcount = 0
			
			decstr = ' '.join(decs)
			decstr = decstr.ljust(cols*3)
				
			chstr = ''.join(chars)
			
			res.append(f'{decstr}| {chstr}')
			decs = []
			chars = []
	
	return '\n'.join(res) + '\n- - - -'
	
#Legacy alias
shorten = shrink_string_end