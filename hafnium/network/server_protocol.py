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

from muodata.repr import *

from ..exceptions import *
from ..utility import *

###############################################################################


class GenericServerProtocol(asyncio.Protocol):


	def __init__(self, router):

		super().__init__()
		self.router = router
		self.transport = None
		
		self.data_dump = []
	
	
	@property
	def sessioned(self):
		return self.router.sessioned
		
		
	@property
	def session(self):
		
		if self.sessioned:
			return self.router.server.get_session_by_transport(self.transport)


	def connection_made(self, transport):
		
		debug_print('Connection established. Client: {}'.format(transport))
		debug_print('Currently on: {} sessions'.format(len(self.router.server.sessions)))
		self.transport = transport


	def data_received(self, data):

		print('Protocol received {} bytes of data.'.format(len(data)))
		self.data_dump.append(data)
		
		try:
			
			response_netpackage, tail = self.router.process_request(b''.join(self.data_dump), transport = self.transport)
			
			if not (response_netpackage.package_code == 5):
				raw_response = response_netpackage.pack()
				
				self.transport.write(raw_response)
				#debug_print(f'Sent response {response_netpackage.package_code}, session_id = {byte_hex_shorthand(response_netpackage.session_id)} ({len(raw_response)} bytes)')
			
			if len(tail)>0:
				self.data_dump = [tail]
			else:
				self.data_dump = []

		except PackageLengthMismatch:
			
			debug_print('Data not enough to form a package. Protocol waiting for more data.')
			pass
			
		except Exception:
			
			self.data_dump = []
			#debug_print(f'Failed to form any response. session_id = {byte_hex_shorthand(self.session.session_id)}')
			raise


	def connection_lost(self, exc):
		
		#debug_print(f'Connection closed. Reason: {exc}')
		self.router.server.close_session_by_transport(self.transport)
	
		#debug_print(f'Currently on: {len(self.router.server.sessions)} sessions')