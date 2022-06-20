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

from typing import Optional, Any
from secrets import token_bytes

###############################################################################

def randbytes(n):
	return token_bytes(n)
	
def signed_int_to_bytes(i: int, bytelen: Optional[int] = None) -> bytes:
	"""
	Represents a signed integer in bytes, in smallest possble
	amount of bytes unless the byte length is specified explicitly.
	Uses two's compliment
	"""

	if not bytelen:
		return i.to_bytes((i.bit_length() + 8) // 8, byteorder="big", signed = True)
	
	else:
		return i.to_bytes(bytelen, byteorder='big', signed = True)

def unsigned_int_to_bytes(i: int, bytelen: Optional[int] = None) -> bytes:
	"""
	Represents an unsigned integer in bytes, in smallest possble
	amount of bytes unless the byte length is specified explicitly
	"""
	
	if i==0:
		if not bytelen: bytelen = 1
		return b'\x00'*bytelen

	if not bytelen:
		return i.to_bytes((i.bit_length() + 7) // 8, byteorder="big")
	
	else: 
		return i.to_bytes(bytelen, byteorder='big')

def bytes_to_signed_int(b: bytes) -> int:
	"""
	Converts bytes into a signed integer (using the
	two's compliment convention), if possible
	"""
	
	return int.from_bytes(b, byteorder='big', signed = True)

def bytes_to_unsigned_int(b: bytes) -> int:
	"""
	Converts bytes into a unnsigned integer, if possible
	"""
	
	return int.from_bytes(b, byteorder='big')

def bytes_bits(b: bytes, padding = True) -> str:
	"""
	Represents bytes as stings of ones and zeros, padding each eight bits
	"""
	
	masks = [
		int('10000000',2),
		int('01000000',2),
		int('00100000',2),
		int('00010000',2),
		int('00001000',2),
		int('00000100',2),
		int('00000010',2),
		int('00000001',2)
		]
	
	res = ''
	
	for bt in b:
		
		for m in masks:
			res += '1' if m&bt else '0'
		
		if padding:	
			res += ' '
		
	return res
	
def right_bits(b: Any, i: int) -> str:
	
	if isinstance(b, int):
		b = unsigned_int_to_bytes(b, bytelen=2+int(i/8.0))
			
	bits = bytes_bits(b, padding = False)
	return bits[-min(len(bits),i):]
	
	
	
def bit_not(n, numbits=32):
    return (1 << numbits) - 1 - n


def succinct_len(i: int) -> bytes:
	"""
	Represents i as a sequence of bytes (h, l),
	where l is a minimal byte representation of int i,
	and h is one byte representing the length of l
	"""
	
	l = unsigned_int_to_bytes(i)
	h = unsigned_int_to_bytes(len(l), bytelen = 1)
		
	return h+l
	
def intlist_to_bytes(lst):
	
	return b''.join([unsigned_int_to_bytes(i, bytelen=1) for i in lst])

def intlist_bin_xor(lst, lst2):
	
	maxlen = max(len(lst), len(lst2))
	
	res = []
	
	for i in range(0, maxlen):
		res.append( lst[i%len(lst)] ^ lst2[i%len(lst2)] )
	
	return res
	
def intlist_bin_and(lst, lst2):
	
	maxlen = max(len(lst), len(lst2))
	
	res = []
	
	for i in range(0, maxlen):
		res.append( lst[i%len(lst)] & lst2[i%len(lst2)] )
	
	return res
	
def intlist_bin_multixor(*args):
	
	res = args[0]
	i = 1
	while i<len(args):
		res = intlist_bin_xor(res, args[i])
		i+=1
	return res
	
		