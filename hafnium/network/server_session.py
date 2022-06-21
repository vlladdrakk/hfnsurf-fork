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

from muodata.repr import *

from ..exceptions import *
from ..utility import *

###############################################################################

class GenericServerSession:
	"""A session connected to the socket server, consisting
	of the mainpipe and the listener
	"""

	def __init__(self, session_id):

		self.session_id = session_id
		
		self.mainpipe = None
		self.listener = None

	def set_mainpipe(self, transport):

		if transport:
			
			self.mainpipe = transport
			self.mainpipe.session_id = self.session_id
			
			return True
			
		return False

	def set_listener(self, transport):

		if transport:
			
			self.listener = transport
			self.listener.session_id = self.session_id
			
			return True
			
		return False

	def send_to_mainpipe(self, netpackage, raw=False):

		try:
			if self.mainpipe:
				
				if not raw:
					netpackage = netpackage.pack()
	
				self.mainpipe.write(netpackage)
		
		except PackFailure as e:
			
			debug_print('Failed to send netpackage to mainpipe {byte_hex_shorthand(self.session_id)}')
			raise e
		
		except:
			
			debug_print('Failed to send netpackage to mainpipe {byte_hex_shorthand(self.session_id)}')
			raise DataTransferFailure
			
	def send_to_listener(self, netpackage, raw=False):

		try:
			if self.listener:
				
				if not raw:
					netpackage = netpackage.pack()
	
				self.listener.write(netpackage)

		except PackFailure as e:
			debug_print('Failed to send netpackage to listener {byte_hex_shorthand(self.session_id)}')
			raise e
		
		except:
			debug_print('Failed to send netpackage to listener {byte_hex_shorthand(self.session_id)}')
			raise DataTransferFailure
			
	def pretty_print(self):

		print('= = = Session representation begin = = =')
		print(':: session_id :: {}'.format(byte_hex_shorthand(self.session_id)))
		print(':: mainpipe :: {}'.format(self.mainpipe))
		print(':: listener :: {}'.format(self.listener))
		print('= = = Session representation end = = =')

	def close(self):

		try:
			self.mainpipe.close()
			
		except:
			debug_print('Failed to properly close server session mainpipe {byte_hex_shorthand(self.session_id)}')
			raise

		try:
			if self.listener:
				self.listener.close()
		except:
			debug_print('Failed to properly close server session listener {byte_hex_shorthand(self.session_id)}')
			raise

		self.mainpipe = None
		self.listener = None
