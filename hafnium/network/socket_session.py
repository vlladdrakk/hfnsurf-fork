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

from typing import Optional
from time import sleep

from .sockets import *
from .netpackage import *
from ..utility import *

###############################################################################


class OneWaySocketSession:

	def __init__(self, host, port):

		self.session_id = None

		self.host = host
		self.port = port

		self.mainpipe = None

		self.incoming_queue = []

	def is_connected(self):

		return not (self.mainpipe == None)

	def drop(self):

		self.host = None
		self.port = None

		self.mainpipe = None

		self.session_id = None

	def send_netpackage(self, np, noreply = False):

		sck = self.mainpipe
		sck.send_netpackage(np)

		if not noreply:
			
			np = None
			
			while not np:
				np = sck.read_from_socket()

			return np
		
	def connect(self, host, port):

		self.host = host
		self.port = int(port)
		self.initialize_connection()

	def initialize_connection(self):

		self.mainpipe = GenericSocket(self.host, self.port)

		self.mainpipe.connect()

		np = CreateSessionPackage()
		self.session_id = np.session_id

		result_np = self.send_netpackage(np)



class GenericSocketSession:


	def __init__(self, host: str,
					 	port: int,
						blocking: bool = True,
						threaded: bool = False,
						timeout: int = 4,
						readlen: int = 256):

		self.session_id = None

		self.host = host
		self.port = port

		self.blocking = blocking
		self.threaded = threaded
		
		self.readlen = readlen
		self.timeout = timeout
		
		self.drop()


	def is_connected(self):
		
		if self.mainpipe and self.listener:
			return (self.mainpipe.connected and self.listener.connected)
		
		return False


	def drop(self):
		
		self.mainpipe = None
		self.listener = None

		self.incoming_queue = []
		
		
	def connect(self, host, port):

		self.host = host
		self.port = int(port)
		self.initialize_connection()
		
		
	def generate_create_session_package(self):
		
		return CreateSessionPackage()
		
		
	def initialize_connection(self):
		
		self.mainpipe = GenericSocket(self.host,
										self.port,
										socket_session = self,
										timeout = self.timeout,
										readlen = self.readlen)

		self.mainpipe.connect()
		
		np = self.generate_create_session_package()
		self.session_id = np.session_id
		
		result_np = self.send_netpackage(np)
		
		if result_np.status == 'success':
			
			self.listener = GenericSocket(self.host,
											self.port,
											blocking = self.blocking,
											threaded = self.threaded,
											socket_session = self,
											timeout = self.timeout,
											readlen = self.readlen)
			
			self.listener.connect()
			
			np = AssignListenerPackage(self.session_id)
			result_np = self.send_netpackage(np, listener = True)
			
			if result_np.status == 'success':
				
				if self.threaded:
					self.run_listener()
					
				return True
		
		self.drop()
		return False
		
	
	def send_netpackage(self, np: NetPackage,
								listener: bool = False,
								noreply: bool = False) -> Optional[NetPackage]:
			
		sck = self.mainpipe
		if listener: sck = self.listener
		
		if sck:
			
			sck.send_netpackage(np)
			
			if not noreply:
				
				np = None
				
				while not np:
					np = sck.read_from_socket()
					
				return np
			
	def run_listener(self):

		if self.threaded:
			self.listener.thread.start()
			
			
	def handle_queue(self):

		while len(self.incoming_queue)>0:
			self.handle_netpackage(self.incoming_queue.pop(0))


	def handle_netpackage(self, np):

		pass