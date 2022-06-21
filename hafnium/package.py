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

import hashlib

from muodata.repr import *
from muodata.binary import *

from .element import *
from .bytecoders import *
from .utility import *
from .exceptions import *

###############################################################################


class Package:


	def __init__(self):

		self.initialize()


	def initialize(self):

		self._elements = dict()
		self._preset_tp_codes = dict()


	@property
	def list_element_names(self):
		
		return [element.name for name, element in self._elements.items()]


	def add_element(self, name, val, tp_code = None):

		new_element = Element(name, val, tp_code = tp_code)
		self._elements[new_element.name] = new_element


	def has_element(self, name):

		if str(name) in self._elements:
			return True
			
		return False


	def get_element(self, name):
		
		if self.has_element(str(name)):
			return self._elements[str(name)]
		
		debug_print('Wrong element name: {}'.format(name))	
		raise WrongElementName
		
		
	def get_packed_element(self, name):

		if self.has_element(str(name)):
			return self._elements[str(name)].pack()
			
		debug_print('Wrong element name: {}'.format(name))	
		raise WrongElementName
		
		
	def get_value(self, name):

		return self.get_element(name).value


	def set_value(self, name, val, tp_code = None):

		if self.has_element(name):
			
			element = self.get_element(name)
			element.tp_code = tp_code
			element.value = val
			
		else:

			if name in self._preset_tp_codes:
				tp_code = self._preset_tp_codes.pop(name)

			self.add_element(name, val, tp_code = tp_code)


	def set_tp_code(self, name, tp_code):

		if self.has_element(name):
			
			element = self.get_element(name)
			element.tp_code = tp_code
			
		else:
			self._preset_tp_codes[name] = tp_code
	
	
	def pack(self, ignore_hash = False):
		
		try:
			count = succinct_len(len(self._elements))
			packed = b''.join([self.get_packed_element(name) for name in self._elements])
									
			if ignore_hash:
				byte_hash = b'0'*32
				
			else:
				
				hasher = hashlib.sha256()
				hasher.update(packed)
				byte_hash = hasher.digest()
				
			full_len = succinct_len(len(byte_hash) + len(count) + len(packed))
			res = b''.join([full_len, byte_hash, count, packed])
			
			return b''.join([full_len, byte_hash, count, packed])
		
		except:
			
			debug_print('Exception during packing:')
			raise PackFailure


	def unpack(self, byte_stream, ignore_hash = False):
		
		try:
			
			mem_stream = memoryview(byte_stream)
			
			self.initialize()
			cursor = 0
			
			def slice_bytes(shift):
				
				nonlocal cursor, mem_stream
				cursor += shift
				return mem_stream[cursor-shift:cursor].tobytes()
					
			full_len_flag = bytes_to_unsigned_int(slice_bytes(1))
			full_len = bytes_to_unsigned_int(slice_bytes(full_len_flag))
			
			if full_len > len(mem_stream[cursor:]):
				raise PackageLengthMismatch
				
			byte_hash_check = slice_bytes(32)
			
			count_flag = bytes_to_unsigned_int(slice_bytes(1))
			count = bytes_to_unsigned_int(slice_bytes(count_flag))
			
			if ignore_hash:
				byte_hash = b'0'*32
				
			else:
				hasher = hashlib.sha256()
				hasher.update(mem_stream[cursor:full_len+1+full_len_flag])
				byte_hash = hasher.digest()
			
			if ignore_hash or (byte_hash == byte_hash_check) :
				
				for c in range(count,0,-1):
	
					new_element = Element(None,None)
					cursor = new_element.unpack(mem_stream, cursor)
					self._elements[new_element.name] = new_element
				
				return mem_stream[cursor:]
			
			else:
				
				raise HashMismatch
		
		except (PackageLengthMismatch, HashMismatch) as e:
			
			debug_print('Exception during unpacking:')
			raise e
		
		except:
			
			debug_print('Exception during unpacking:')
			raise UnpackFailure
			
			
	def pretty_print(self):
	
		print('= = = Package representation begin = = =')
		for name, element in self._elements.items():
			
			val = element.value
			
			if type(val) == bytes:
				val = byte_hex_shorthand(val)
				 
			print('{} :: {} :: {}'.format(shrink_string_end(name,20), shrink_string_end(val,40), shrink_string_end(element.byte_coder_name,30)))

		print('= = = Package representation end = = =')


class PackageObject(Package):


	def __init__(self):

		super().__init__()


	def __getattr__(self, attr):

		if attr in ('_elements','_preset_tp_codes'):
			return self.__dict__[attr]
			
		return self.get_value(attr)


	def __setattr__(self, attr, val):

		if attr in ('_elements','_preset_tp_codes') and (val == dict()):
			self.__dict__[attr] = dict()
			
		elif (attr!='_elements'):
			self.set_value(attr, val)


	def setup_field(self, name, tp_code):

		self.set_tp_code(name, tp_code)
