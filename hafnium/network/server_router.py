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

from .server_session import *
from .netpackage import *

from ..exceptions import *
from ..utility import *

###############################################################################


class GenericServerRouter:

	def __init__(self, server):

		self.server = server

	def process_request(self, raw_request, transport = None):
	
		request, tail = self.custom_prepare_before_route(raw_request, transport = transport)
		response = self.route_request(request, transport = transport)			

		return response, tail

	def custom_prepare_before_route(self, raw_request, transport = None):

		return raw_request

	def route_request(self, request, transport = None):

		return request



class HafniumServerRouter(GenericServerRouter):

	def __init__(self, server, sessioned = True):

		super().__init__(server)
		self.request_handlers = dict()
		self.sessioned = sessioned
		
		self.register_request_handler(CREATE_SESSION_REQUEST,
								self.handle_create_session)
		
		self.register_request_handler(ASSIGN_LISTENER_REQUEST,
								self.handle_assign_listener)
		
		self.register_request_handler(ECHO_REQUEST,
								self.handle_echo)

	def register_request_handler(self, request_code, handler_func):
		
		self.request_handlers[request_code] = handler_func

	def custom_prepare_before_route(self, raw_request, transport = None):

		request_netpackage = NetPackage(None, None)
		tail = request_netpackage.unpack(raw_request)

		return request_netpackage, tail


	def route_request(self, request, transport = None):
		
		#try:
		if True:
				
			try:
				session_id = request.session_id
				# debug_print(f'Routing request {request.package_code}, session_id = {byte_hex_shorthand(request.session_id)}')
				
			except:
				raise SessionIDNotProvided
				
			if request.package_code == CREATE_SESSION_REQUEST:
				resp = self.handle_create_session(request, session_id, transport = transport)
			
			else:
				
				if self.sessioned:
					try:
						session = self.server.get_session(session_id)
					
					except:
						debug_print('Session not found. Sending a failure request.')
						return FailureNetPackage(session_id)
				
				else:
					session = None
					
				if request.package_code in self.request_handlers:
					resp = self.request_handlers[request.package_code](request, session, transport = transport)
				
				else:
					resp = self.custom_route_request(request, session, transport = transport)
					
			if not resp:
				debug_print('Failed to form a response. Sending a failure request.')
				return FailureNetPackage(session_id)
				
			return resp
		
		#except Exception as e:
		
		#	debug_print('Exception during routing the request. Sending a failure request.')
		#	debug_print(f'!!! {e}')
		#	return FailureNetPackage(session_id)
		

	def custom_route_request(self, request, session, transport = None):

		return None
	
	###
	# REQUEST HANDLERS
	###
	
	def handle_create_session(self, request, session_id, transport = None):
		
		new_session = GenericServerSession(session_id)
		result = new_session.set_mainpipe(transport)
					
		if result:
					
			self.server.add_session(new_session)
			return SuccessNetPackage(session_id)
	
	def handle_assign_listener(self, request, session, transport = None):
		
		result = session.set_listener(transport)

		if result:
				
			session.pretty_print()
			return SuccessNetPackage(session.session_id)

	
	def handle_echo(self, request, session, transport = None):
		
		return request