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

import struct

from datetime import date, datetime
from decimal import Decimal

from muodata.binary import *
from muodata.dates import *

from .exceptions import *
from .utility import *

###################################


class GenericByteCoder:

	def __init__(self):

		self.expected_type = None

	def ensure_type(self, val):

		if not isinstance(val, self.expected_type):
			raise TypeMismatch(self.expected_type, type(val))

	def to_bytes(self, val):
		
		try:
			
			self.ensure_type(val)
			result_bytes = self.to_bytes_convert(val)
					
			return result_bytes
			
		except:
			
			debug_print('Exception in bytecoder')
			raise ByteCoderToBytesFailure
	
	def from_bytes(self, val):

		try:
			
			result = self.from_bytes_convert(val)
			self.ensure_type(result)
			
			return result	
			
		except:
			
			debug_print('Exception in bytecoder')
			raise ByteCoderFromBytesFailure

	def to_bytes_convert(self, val):
		"""Custom convert function"""
		pass

	def from_bytes_convert(self, val):
		"""Custom convert function"""
		pass


class ByteByteCoder(GenericByteCoder):

	def __init__(self):

		super().__init__()
		self.expected_type = bytes

	def to_bytes_convert(self, val):
		return val

	def from_bytes_convert(self, val):
		return val


class StringByteCoder(GenericByteCoder):

	def __init__(self):

		super().__init__()
		self.expected_type = str

	def to_bytes_convert(self, val):		
		return bytes(val.encode('utf-8'))

	def from_bytes_convert(self, val):		
		return val.decode('utf-8')


class IntegerByteCoder(GenericByteCoder):

	def __init__(self):

		super().__init__()
		self.expected_type = int

	def to_bytes_convert(self, val):		
		return signed_int_to_bytes(val)
	
	def from_bytes_convert(self, val):
		return bytes_to_signed_int(val)
	

class ListByteCoder(GenericByteCoder):

	def __init__(self):

		super().__init__()
		self.expected_type = list

	def to_bytes_convert(self, val):
					
		res = []
		
		for v in val:
			
			if type(v) in BASIC_TYPES:
				
				tp_code = BASIC_TYPES[type(v)]
				bytecoder = BYTE_CODERS[tp_code]
				v_bytes = bytecoder.to_bytes(v)
				l_bytes = len(v_bytes)
				
				res.append(unsigned_int_to_bytes(tp_code, bytelen = 2))
				res.append(succinct_len(l_bytes))
				res.append(v_bytes)
				
			else:
				raise MemberTypeUnknown
		
		return b''.join(res)


	def from_bytes_convert(self, val):
		
		cursor = 0
		
		def slice_bytes(shift):
			
			nonlocal cursor, memval
			cursor += shift
			return memval[cursor-shift:cursor].tobytes()
		
		memval = memoryview(val)
		res = []
		
		while cursor < len(memval):
			
			tpcode = bytes_to_unsigned_int(slice_bytes(2))
			l_bytes_flag = bytes_to_unsigned_int(slice_bytes(1))
			l_bytes = bytes_to_unsigned_int(slice_bytes(l_bytes_flag))

			bytecoder = BYTE_CODERS[tpcode]			
			res.append(bytecoder.from_bytes(slice_bytes(l_bytes)))
			
		return res


class DictByteCoder(GenericByteCoder):

	def __init__(self):

		super().__init__()
		self.expected_type = dict

	def to_bytes_convert(self, val):

		res = list()
		
		for key, dict_val in val.items():

			for v in (key, dict_val):

				if type(v) in BASIC_TYPES:
					
					tp_code = BASIC_TYPES[type(v)]
					bytecoder = BYTE_CODERS[tp_code]
					v_bytes = bytecoder.to_bytes(v)
					l_bytes = len(v_bytes)

					res.append(unsigned_int_to_bytes(tp_code, bytelen = 2))
					res.append(succinct_len(l_bytes))
					res.append(v_bytes)

				else:
					raise MemberTypeUnknown

		return b''.join(res)
		

	def from_bytes_convert(self, val):
		
		cursor = 0
		
		def slice_bytes(shift):
			
			nonlocal cursor, memval
			cursor += shift
			return memval[cursor-shift:cursor].tobytes()
		
		memval = memoryview(val)
		res = dict()

		current_key = None
		
		while cursor < len(memval):

			tpcode = bytes_to_unsigned_int(slice_bytes(2))
			l_bytes_flag = bytes_to_unsigned_int(slice_bytes(1))
			l_bytes = bytes_to_unsigned_int(slice_bytes(l_bytes_flag))
			
			bytecoder = BYTE_CODERS[tpcode]
			res_v = bytecoder.from_bytes(slice_bytes(l_bytes))

			if current_key == None:
				current_key = res_v
				
			else:
				
				res[current_key] = res_v
				current_key = None

		return res


class FloatByteCoder(GenericByteCoder):

	def __init__(self):

		super().__init__()
		self.expected_type = float

	def to_bytes_convert(self, val):
		return struct.pack('>d', val)
		
	def from_bytes_convert(self, val):
		return struct.unpack('>d', val)[0]
		

class DateByteCoder(GenericByteCoder):

	def __init__(self):

		super().__init__()
		self.expected_type = date

	def to_bytes_convert(self, val):
		
		return date_to_4_bytes(val)

	def from_bytes_convert(self, val):
		
		return date_from_4_bytes(val)


class DecimalByteCoder(GenericByteCoder):

	def __init__(self):

		super().__init__()
		self.expected_type = Decimal

	def to_bytes_convert(self, val):
		
		return bytes(str(val).encode('utf-8'))
			
	def from_bytes_convert(self, val):
					
		return Decimal(val.decode('utf-8'))
	
	
class TupleByteCoder(GenericByteCoder):

	def __init__(self):

		super().__init__()
		self.expected_type = tuple

	def to_bytes_convert(self, val):
		
		val = list(val)
		bytecoder = BYTE_CODERS[LIST_TP_CODE]
		
		return bytecoder.to_bytes(val)
	
	def from_bytes_convert(self, val):
		
		bytecoder = BYTE_CODERS[LIST_TP_CODE]
		
		return tuple(bytecoder.from_bytes(val))
	
	
class SetByteCoder(GenericByteCoder):

	def __init__(self):

		super().__init__()
		self.expected_type = set

	def to_bytes_convert(self, val):
		
		val = list(val)
		bytecoder = BYTE_CODERS[LIST_TP_CODE]
		
		return bytecoder.to_bytes(val)

	def from_bytes_convert(self, val):
		
		bytecoder = BYTE_CODERS[LIST_TP_CODE]
		
		return set(bytecoder.from_bytes(val))
	
	
class NoneTypeByteCoder(GenericByteCoder):

	def __init__(self):

		super().__init__()
		self.expected_type = type(None)

	def to_bytes_convert(self, val):
		return b''

	def from_bytes_convert(self, val):
		return None
	
	
class BooleanByteCoder(GenericByteCoder):

	def __init__(self):

		super().__init__()
		self.expected_type = bool

	def to_bytes_convert(self, val):
		
		if val:
			return unsigned_int_to_bytes(1, bytelen = 1)
		
		else:
			return unsigned_int_to_bytes(0, bytelen = 1)

	def from_bytes_convert(self, val):
		
		if bytes_to_unsigned_int(val) == 1:
			return True
		
		else:
			return False


class DateTimeByteCoder(GenericByteCoder):

	def __init__(self):

		super().__init__()
		self.expected_type = date

	def to_bytes_convert(self, val):
		
		return datetime_to_7_bytes(val)

	def from_bytes_convert(self, val):

		return datetime_from_7_bytes(val)


BYTES_TP_CODE = 10
STRING_TP_CODE = 11
INTEGER_TP_CODE = 12
FLOAT_TP_CODE = 13
NONE_TP_CODE = 14
BOOLEAN_TP_CODE = 15
LIST_TP_CODE = 16
DICT_TP_CODE = 17
DATE_TP_CODE = 111
DECIMAL_TP_CODE = 112
TUPLE_TP_CODE = 113
SET_TP_CODE = 114
DATETIME_TP_CODE = 115
	
	
BASIC_TYPES = {
	bytes: BYTES_TP_CODE,
	str: STRING_TP_CODE,
	int: INTEGER_TP_CODE,
	float: FLOAT_TP_CODE,
	type(None): NONE_TP_CODE,
	bool: BOOLEAN_TP_CODE,
	list: LIST_TP_CODE,
	dict: DICT_TP_CODE,
	date: DATE_TP_CODE,
	Decimal: DECIMAL_TP_CODE,
	tuple: TUPLE_TP_CODE,
	set: SET_TP_CODE,
	datetime: DATETIME_TP_CODE
	}
	

BYTE_CODERS = {
	BYTES_TP_CODE: ByteByteCoder(),
	STRING_TP_CODE: StringByteCoder(),
	INTEGER_TP_CODE: IntegerByteCoder(),
	FLOAT_TP_CODE: FloatByteCoder(),
	NONE_TP_CODE: NoneTypeByteCoder(),
	BOOLEAN_TP_CODE: BooleanByteCoder(),
	LIST_TP_CODE: ListByteCoder(),
	DICT_TP_CODE: DictByteCoder(),
	DATE_TP_CODE: DateByteCoder(),
	DECIMAL_TP_CODE: DecimalByteCoder(),
	TUPLE_TP_CODE: TupleByteCoder(),
	SET_TP_CODE: SetByteCoder(),
	DATETIME_TP_CODE: DateTimeByteCoder()
	}
	
