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

import socket
import threading

from muodata.binary import *
from muodata.repr import *

from .netpackage import *
from ..utility import *
from ..exceptions import *

###############################################################################


class GenericSocket:
	

	def __init__(self, host: str,
						port: int,
						blocking: bool = True,
						threaded: bool = False,
						socket_session: Optional["GenericSocketSession"] = None,
						timeout: int = 4,
						readlen: int = 256):
						
		self.host = host
		self.port = port		
		
		self.blocking = blocking
		self.threaded = threaded
		self.socket_session = socket_session
		self.readlen = readlen

		self.underlying_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.underlying_socket.settimeout(timeout)
		
		self.incoming_bytes_reader = bytes()
		
		# debug_print(f'Socket initialized. {self.underlying_socket}')
		
		self.connected = False
		
		if self.threaded:
			
			self.underlying_socket.settimeout(None)
			self.thread = threading.Thread(target=self.process_listener_queue, daemon=True)
		
	
	def process_listener_queue(self):

		while True:

			np = None
			
			while not np:
				np = self.read_from_socket()

			self.socket_session.incoming_queue.append(np)
			self.socket_session.handle_queue()
			
			
	def disconnect(self):
		
		debug_print("* * *ENTERED DISCONNECT")
		self.connected = False
		
		if self.socket_session:
			self.socket_session.drop()


	def connect(self):
		
		try:
			
			self.underlying_socket.connect((self.host, self.port))
			self.connected = True
			
			# debug_print(f'Socket connnected. {self.host}:{self.port}')
			
			if not self.blocking:
				self.underlying_socket.settimeout(0.0)
				
		except:
			
			debug_print('Socket failed to connect" {self.host}:{self.port}')
			self.disconnect()
			
			raise

	def send_netpackage(self, np):
		
		try:
			self.underlying_socket.sendall(np.pack())
			# debug_print(f'Netpackage sent: session_id={byte_hex_shorthand(np.session_id)} code={np.package_code}')
		
		except PackFailure:
			debug_print('Failed to send netpackage due to package error')
			raise
			
		except:
						
			debug_print('Failed to send netpackage via socket')
			self.disconnect()
			raise
			

	def set_timeout(self, seconds):		
		self.underlying_socket.settimeout(seconds)
		
		
	def handle_chunk_test(self, chunk):
			
		cursor = 0
		mem_stream = memoryview(chunk)
		
		def slice_bytes(shift, return_view: bool = False):
				
			nonlocal cursor, mem_stream
			cursor += shift
			
			if return_view:
				return mem_stream[cursor-shift:cursor]
			else:
				return mem_stream[cursor-shift:cursor].tobytes()
		
		np = None
						
		expected_length = -1
			
		self.incoming_bytes_reader += chunk
		
		if expected_length < 0:
			
			full_len_flag = bytes_to_unsigned_int(slice_bytes(1))
			expected_length = bytes_to_unsigned_int(slice_bytes(full_len_flag))
			
		cursor = 0
		cutoff = expected_length + 1 + full_len_flag
		
		if len(mem_stream) >= cutoff:
			
			incoming_bytes = self.incoming_bytes_reader[:cutoff]
			
			self.incoming_bytes_reader = self.incoming_bytes_reader[cutoff:]
			np = self.form_netpackage_from_bytes(incoming_bytes)
			
			expected_length = -1
		
		return np
		
		
	def handle_chunk(self, chunk):
		
		np = None
						
		expected_length = -1
			
		self.incoming_bytes_reader += chunk
		
		if expected_length < 0:
			
			full_len_flag = bytes_to_unsigned_int(self.incoming_bytes_reader[0:1])
			expected_length = bytes_to_unsigned_int(self.incoming_bytes_reader[1:1+full_len_flag])
			
		cutoff = expected_length + 1 + full_len_flag
		
		if len(self.incoming_bytes_reader) >= cutoff:
			
			incoming_bytes = self.incoming_bytes_reader[:cutoff]
			
			self.incoming_bytes_reader = self.incoming_bytes_reader[cutoff:]
			np = self.form_netpackage_from_bytes(incoming_bytes)
			
			expected_length = -1
		
		return np
			
					
	def read_from_socket(self):

		try:
	
			chunk = self.underlying_socket.recv(self.readlen)
			
			if (not self.blocking) and chunk == b'':
				
				self.disconnect()
				debug_print('Received empty byte from socket')
				
				raise
	
			if chunk:
				return self.handle_chunk(chunk)
			
			return None
		
		except:
			
			if self.blocking:
				
				debug_print('Failed to read from socket')
				self.disconnect()
				raise
			
			return None
	
	def form_netpackage_from_bytes(self, b):
		
		np = NetPackage(None, None)
		np.unpack(b)
		
		return np
		