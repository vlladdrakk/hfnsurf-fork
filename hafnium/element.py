# Copyright (c) 2022 Keith Aprilnight
# 
# This file is part of hafnium and is licenced under the terms of MIT License.
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

from muodata.binary import *

from .bytecoders import *

###################################

class Element:
	"""This class represents a singular, atomic element of
	a hafnium package.
	"""

	def __init__(self, name, value, tp_code = None):
		"""Initializes an element.
		
		If the tp_code argument is set,
		this element will be forced to use a particular bytecoder type.
		
		If it's not set, the bytecoder type will be assumed from the value
		type, if it exists in the bytecoders library."""

		self.initialize()
		self.tp_code = tp_code

		if name!=None:
			self.name = name
			
		self.value = value
		
	def initialize(self):
		
		self.__name = None
		self.__value = None
		
	@property
	def byte_coder(self):	
		
		try:
			return BYTE_CODERS[self.tp_code]
			
		except:
			raise ByteCoderNotFoundException

	@property
	def byte_coder_name(self):
		
		if self.tp_code in BYTE_CODERS:
			return str(BYTE_CODERS[self.tp_code].__class__.__name__)
		
		else:
			return 'NO_BYTECODER'

	@property
	def name(self):
		
		return self.__name

	@property
	def value(self):
		
		return self.__value

	@name.setter
	def name(self, val):
		
		self.__name = val

	@value.setter
	def value(self, val):
		
		if val == None:
			self.tp_code = 14
			
		elif (type(val) in BASIC_TYPES) and (self.tp_code == None):
			self.tp_code = BASIC_TYPES[type(val)]
			
		self.__value = val
		
	@property
	def packed_name(self):	
		
		try:
			return BYTE_CODERS[STRING_TP_CODE].to_bytes(self.__name)
			
		except:
			raise ByteCoderNotFoundException
	
	@property
	def packed_value(self):		
		return self.byte_coder.to_bytes(self.__value)
	
	def unpack_name(self, b):
		
		try:
			self.name = BYTE_CODERS[STRING_TP_CODE].from_bytes(b)
			
		except:
			raise ByteCoderNotFoundException
		
	def unpack_value(self, b):
		self.value = self.byte_coder.from_bytes(b)

	def pack(self):
		
		try:
			
			packed_name = self.packed_name
			packed_value = self.packed_value
			
			res = [succinct_len(len(packed_name))]
			res.append(packed_name)
			res.append(unsigned_int_to_bytes(self.tp_code, bytelen = 2))
			res.append(succinct_len(len(packed_value)))
			res.append(packed_value)
	
			return b''.join(res)
		
		except:
			raise ElementPackFailure

			
	def unpack(self, mem_stream, cursor):
		
		try:
			
			def slice_bytes(shift):
				
				nonlocal cursor, mem_stream
				cursor += shift
				return mem_stream[cursor-shift:cursor].tobytes()
					
			namelen_flag = bytes_to_unsigned_int(slice_bytes(1))
			namelen = bytes_to_unsigned_int(slice_bytes(namelen_flag))
			
			self.unpack_name(slice_bytes(namelen))
	
			self.tp_code = int.from_bytes(slice_bytes(2), byteorder='big')
	
			vallen_flag = bytes_to_unsigned_int(slice_bytes(1))
			vallen = bytes_to_unsigned_int(slice_bytes(vallen_flag))
			
			self.unpack_value(slice_bytes(vallen))
	
			return cursor
		
		except:
			raise ElementUnpackFailure
