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

from .bases import *
from .ascii import *
	
###############################################################################

def hexstring_to_hexbytelist(s):
	
	res = []
	s = s.upper()
	
	if len(s)%2==0:

		while s:
			res.append(s[:2])
			s = s[2:]
	
	return res
	
def intlist_hexdump(src_lst, cols = 8):
	
	lst = src_lst[::]
	res = [f'- - - -\nhexdump: {len(lst)} bytes']

	colcount = 0
	hexes = []
	chars = []
	
	while len(lst)>0:
		
		bt = lst.pop(0)
			
		hex = base_translate(bt, 10, 16, pad_width=2)
		ch = int_to_ascii(bt, control_replace = True)
			
		hexes.append(hex)
		chars.append(ch)
				
		colcount += 1
		
		if (colcount == cols) or (len(lst)==0):
			colcount = 0
			
			hexstr = ' '.join(hexes)
			hexstr = hexstr.ljust(cols*3)
				
			chstr = ''.join(chars)
			
			res.append(f'{hexstr}| {chstr}')
			hexes = []
			chars = []
		
	return '\n'.join(res) + '\n- - - -'
		
def intlist_hexdump_4(lst):
	
	return intlist_hexdump(lst, cols=4)
	
	
def intlist_hexdump_8(lst):
	
	return intlist_hexdump(lst, cols=8)
	
def intlist_hexdump_16(lst):
	
	return intlist_hexdump(lst, cols=16)