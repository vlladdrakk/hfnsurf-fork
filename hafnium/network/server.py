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

import asyncio
import time 

from .server_protocol import *
from ..exceptions import *
from ..utility import *

###################################


class GenericServer:


	def __init__(self, host, port, router = None):

		self.host = host
		self.port = port

		self.router = router

		self.sessions = dict()


	def set_router(self, router):

		self.router = router


	def binded_protocol_factory(self):

		return GenericServerProtocol(self.router)


	def add_session(self, session):

		self.sessions[session.session_id] = session


	def get_session(self, session_id):

		if session_id in self.sessions:
			return self.sessions[session_id]
			
		else:
			raise SessionDoesNotExist
			
			
	def get_session_by_transport(self, transport):
		
		for session_id, s in self.sessions.items():

			if transport in (s.mainpipe, s.listener):
				
				return s
		
		
	def close_session_by_transport(self, transport):

		s = self.get_session_by_transport(transport)
		
		if s:
			s.close()
			self.sessions.pop(s.session_id)


	async def run(self):

		try:
			
			loop = asyncio.get_event_loop()
	
			async_server = await loop.create_server(
				self.binded_protocol_factory,
				host = self.host,
				port = self.port
				)
				
			async with async_server:
				
				print ('\nServer initialized. Serving.\n====\n')
				await async_server.serve_forever()
				
		except Exception as e:
			
			print('!! Uncaught exception during server operation: {}'.format(e))
