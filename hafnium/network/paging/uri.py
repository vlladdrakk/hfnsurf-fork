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

from typing import Optional, Any

from quasidomain.convert import *

from muodata.repr import *
from muodata.binary import *
from muodata.hex import *

from .exceptions import *

from ...bytecoders import *

###############################################################################


class URI:
	
	
	@classmethod
	def from_str(cls, uri_str: str):
		
		if uri_str.endswith('/'):
			uri_str = uri_str[:-1]
			
		quasidomain, host, port = None, None, None
		
		plds = uri_str.split('?')[1:]
		uri_str = uri_str.split('?')[0]
		
		components = uri_str.split('/')
		
		if components[0] == 'hfnp:':
			
			components.pop(0)
			components.pop(0)
			
			if ':' in components[0]:
				
				host, port = components.pop(0).split(':',1)
				port = int(port)
				
			elif '.' in components[0]:
				
				quasidomain = components.pop(0)
				
		
		payload = dict()
		for pld in plds:
			
			if '=' in pld:
				pld = pld.split('=',1)
				
				payload[pld[0]] = pld[1]
				
		if host!=None and port!=None:
			
			return cls(host = host, port = port,
						components = components,
						payload = payload)
						
		if quasidomain:
			
			return cls(quasidomain = quasidomain,
						components = components,
						payload = payload)
						
		return cls(components = components,
					payload = payload)
						
	
	def __init__(self, quasidomain: Optional[str] = None,
						host: Optional[str] = None,
						port: Optional[int] = None,
						components: Optional[list[str]] = None,
						payload: Optional[dict[str, Any]] = None):
							
		# Quasidomain in form site_title.appendix
		self._quasidomain = quasidomain
		
		# List of path components on the server,
		# excluding the servername and appendix=
		if not components: self.components = []
		else: self.components = components
				
		# dict of payload information
		if not payload: self.payload = dict()
		else: self.payload = payload
		
		self._host = host
		self._port = port
		
		
	def __str__(self) -> str:
		
		res = []
		
		if self._quasidomain:
			res.append('hfnp:/')
			res.append(self._quasidomain)
			
		elif self._host!=None and self._port!=None:
			res.append('hfnp:/')
			res.append('{}:{}').format(self._host, self._port)
			
		res.extend(self.components)
		res.append(self.payload_repr())
		
		return '/'.join(res)
	
	
	def is_absolute(self) -> bool:
		
		return (self._quasidomain != None) or (self._port != None and self._host != None)
		
		
	def is_relative(self) -> bool:
		
		return not self.is_absolute()
		
		
	@property
	def title(self) -> Optional[str]:
		
		if self._quasidomain and ('.' in self._quasidomain):
			return self._quasidomain.split('.')[0]
		
		
	@property
	def appendix(self) -> Optional[str]:
		
		if self._quasidomain and ('.' in self._quasidomain):
			return self._quasidomain.split('.')[1]
				
		
	@property
	def quasidomain(self) -> Optional[str]:
		
		return self._quasidomain
	
	
	@property
	def host_port(self) -> Optional[list]:
		
		if self._host != None and self._port != None:
			return self._host, self._port
			
		elif self._quasidomain:
			return resolve_appendix(self.appendix, self.title)
			
			
	@property
	def host_port_str(self) -> Optional[str]:
		
		if self._host != None and self._port != None:
			return '{}:{}'.format(self._host, str(self._port))
			
		elif self._quasidomain:
			return resolve_appendix(self.appendix, self.title)
		
			
	def payload_repr(self) -> str:
		
		res = ['']
		
		for key, value in self.payload.items():
			
			if isinstance(value, bytes):
				value = byte_hex_shorthand(value)
				
			elif not isinstance(value, str):
				
				try:
					value = str(value)
					
				except:
					value = "???"
				
			res.append(f"{key}={value}")
			
		return '?'.join(res)
		
	
	def append(self, other: "URI") -> "URI":
		
		components = self.components[::]
		components.extend(other.components)
		
		payload = {k: v for k, v in other.payload.items()}
		
		if self._quasidomain:
			
			return URI(quasidomain = self._quasidomain,
						components = components,
						payload = payload)
						
		elif self._host != None and self._port != None:
			
			return URI(host = self._host,
						port = self._port,
						components = components,
						payload = payload)
		
		else:
			
			return URI(components = components,
						payload = payload)
	
		
	def equals(self, other_uri: "URI", check_host: bool = False) -> bool:
		
		if check_host and (self.is_relative() or other_uri.is_relative()):
			return False
		
		if len(self.components)==len(other_uri.components):
			
			for i in range(0,len(self.components)):
				
				if self.components[i] != other_uri.components[i]:
					return False
			
			if not check_host:
				return True
				
			if check_host and (self.host_port == other.host_port):
				return True
			
		return False
			
			
	def fits(self, other_uri: "URI", check_host: bool = False) -> bool:
		
		if check_host and (self.is_relative() or other_uri.is_relative()):
			return False
		
		for i in range(0,min(len(self.components),len(other_uri.components))):
			
			if self.components[i] != other_uri.components[i]:
				return False
				
		if not check_host:
			return True
				
		if check_host and (self.host_port == other.host_port):
			return True
			
		return False
				
		
	def getpart(self, i: int) -> str:
		
		if i < len(self.components):		
			return self.components[i]
		
		
	def get_payload(self, key: str) -> Any:
		
		if key in self.payload:
			return self.payload[key]
		
		
	def set_payload(self, key: str, value: Any):
		
		self.payload[key] = value



class URIByteCoder(GenericByteCoder):


	def __init__(self):

		super().__init__()
		self.expected_type = URI


	def to_bytes_convert(self, val: "URI") -> bytes:
		
		val = [
			val._quasidomain,
			val._host,
			val._port,
			val.components,
			val.payload
			]
			
		bytecoder = BYTE_CODERS[LIST_TP_CODE]
		
		return bytecoder.to_bytes(val)
	
	
	def from_bytes_convert(self, val: bytes) -> "URI":
				
		bytecoder = BYTE_CODERS[LIST_TP_CODE]
		lst = bytecoder.from_bytes(val)
					
		return URI(quasidomain = lst[0],
					host = lst[1],
					port = lst[2],
					components = lst[3],
					payload = lst[4])
	
	
URI_TP_CODE = 201
	
BASIC_TYPES[URI] = URI_TP_CODE
BYTE_CODERS[URI_TP_CODE] = URIByteCoder()