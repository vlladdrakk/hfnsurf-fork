# Copyright (c) 2022 Keith Aprilnight
# 
# This file is part of quasidomain and is licenced under the terms of MIT License.
# The full text of license is located in the LICENSE file.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

###############################################################################

from muodata.repr import *
from muodata.binary import *
from muodata.hex import *
from muodata.bases import *

from .sdne_libs import *

from ..exceptions import *

###############################################################################


def sdne_encode(s: str, tld_lst = None) -> bytes:
	
	allbits = ''
	i = 0
	
	while i < len(s):
		
		l = s[i]
		
		trigadded = False
		
		if i < len(s)-2:
			
			trig = l+s[i+1]+s[i+2]
			
			if trig in SDNE_2:
				
				num = SDNE_2[trig]
				trigadded = True
				bits = '1' + right_bits(num, 11)
			
				allbits += bits
				i+=2
			
		if not trigadded:
				
			if l in SDNE_2:
				
					num = SDNE_2[l]					
					bits = '1' + right_bits(num, 11)
					
					allbits += bits
					
			elif l in SDNE_1:
				
					num = SDNE_1.index(l)
					bits = '0'+right_bits(num, 5)
					
					allbits += bits
					
			else:
				raise SDNEEncodingFailed
				
		i+=1
	
	if tld_lst:
		allbits += sdne_tld_bits(tld_lst)
	
	while len(allbits)%8 > 0:
		allbits += '0'
			
	res= b''
	while len(allbits)>0:
		
		bt = allbits[:8]
		allbits = allbits[8:]
		res += unsigned_int_to_bytes(int(base_to_dec(bt, 2)),bytelen=1)
	
	return res
		
		
def sdne_decode(b: bytes) -> [str, list[str]]:
	
	s = bytes_bits(b, padding = False)
	cursor, res, tld = 0, '', False
	
	while cursor < len(s):
		
		ss = s[cursor]
		
		if ss == '0':
			
			if cursor+6 < len(s):
				
				portion = s[cursor+1:cursor+6]
				
				if portion == '11111':
					s = s[cursor:]
					tld = True
					break
					
				portion_i = int(base_to_dec(portion, 2))
				res += SDNE_1[portion_i]
				
			cursor+=6
			
		elif ss == '1':
			
			if cursor+12<len(s):
				
				portion = s[cursor+1:cursor+12]
				portion_i = int(base_to_dec(portion, 2))
				
				if portion_i < len(SDNE_2):
					res += list(SDNE_2.keys())[portion_i]
					
				else:
					raise SDNEEncodingFailed
				
			cursor+=12
			
		else: break
		
	tld_lst = []
	if tld:
		tld_lst = sdne_tld_from_bits(s)
		
	return res, tld_lst
	
	
def sdne_tld_bits(tld_lst: list[str]) -> str:
	
	bits='011111'
	
	for tld in tld_lst:
		
		if tld in SDNE_3:
			code = SDNE_3[tld]
			bits += right_bits(code, 11)
			
		else:
			raise SDNEEncodingFailed
			
	return bits
	

def sdne_tld_from_bits(bits: str) -> list[str]:
	
	bits = bits[6:]
	
	res = []
	while (len(bits)>=11):
		
		portion = bits[:11]
		bits = bits[11:]
		portion_i = int(base_to_dec(portion, 2))
		
		if portion_i < len(SDNE_3):
			res.append(list(SDNE_3.keys())[portion_i])
			
		else:
			raise SDNEEncodingFaileds
			
	return res