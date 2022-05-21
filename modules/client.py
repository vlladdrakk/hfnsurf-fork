# Copyright (c) 2022 Keith Aprilnight
# 
# This file is part of hfnsurf and is licenced under the terms of MIT License.
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

from muodata.uid import *

import hafnium.utility

from hafnium.package import *
from hafnium.network.socket_session import *

from hafnium.network.paging.netpackages import *
from hafnium.network.paging.user import *
from hafnium.network.paging.uri import *
from hafnium.network.paging.processors import *

from modules.view import *
from modules.user_storage import *
from modules.internal_dispatcher import *

###############################################################################

class Client:
	
	debug = True
	
	def __init__(self, browser):
		
		self.browser = browser
		
		self.user_storage = UserStorage(self)
		self.page_view = PageView(self)
		
		self.internal_dispatcher = InternalDispatcher(self)
					
		self.processors = {'generic': GenericClientSideProcessor('generic')} # {name: Processor}
		
		self.current_uri = None
		self.current_ext_uri = None
		
		try:
		#if True:
			self.load_state()
		except:
			self.save_state()
		
	
	def save_state(self):
		
		sv = PackageObject()
		
		sv.users = self.user_storage.save_state()
		sv.processors = self.save_processors_state()
		
		with open('config.bin', 'wb') as cfg:
			cfg.write(sv.pack())
	
	def load_state(self):
		
		with open('config.bin', 'rb') as cfg:
			statebin = cfg.read()
			
		sv = PackageObject()
		sv.unpack(statebin)
			
		self.user_storage.load_state(sv.users)
		
		
	def save_processors_state(self):
		
		return dict()
				
		
	def send_netpackage(self, host, port, np):
		
		session = OneWaySocketSession(host, port)
		session.connect(host, port)
		
		np.session_id = session.session_id
		
		response = session.send_netpackage(np)
		session.mainpipe.underlying_socket.close()
		
		if self.debug:
			print(f'\n- - - RESPONSE CODE: {response.package_code} - - -\n')
			
		return response
		
		
	def send_handshake(self, host, port):
		
		sequence_id = new_uuid()
		
		np = HandshakeRequest()
		np.set_sequence_id(sequence_id)
		
		resp = self.send_netpackage(host, port, np)
		
		return sequence_id, resp.req_queue, resp.resp_queue, resp.sequence_data
		
		
	def send_request(self, host, port, np):
		
		sequence_id, req_queue, resp_queue, sequence_data = self.send_handshake(host, port)
		np.set_sequence_id(sequence_id)
		
		for proc_name in sequence_data:
			
			if proc_name in self.processors:
				processor = self.processors[proc_name]
				processor.accept_sequence_data(sequence_data[proc_name])
		
		for proc_name in req_queue:
			
			if (proc_name in self.processors):
				
				processor = self.processors[proc_name]
				np = processor.additionally_process_request(np)
				
		resp = self.send_netpackage(host, port, np)
		
		for proc_name in resp_queue:
			
			if (proc_name in self.processors):
				
				processor = self.processors[proc_name]				
				resp = processor.additionally_process_response(resp)
				
		return resp
		
		
	def request_page(self, uri):
		
		if uri.host_port == ('0.0.0.0', 0):
			
			user = self.user_storage.get_user_by_uri(self.current_ext_uri)
			content, links, blobs, action_result, uri = self.internal_dispatcher.handle_uri(user, uri)
						
			if content:
								
				self.page_view.content = content
				self.page_view.links = dict()
				
				for linkno, linklst in links.items():
					self.page_view.links[linkno] = URI.from_link(linklst)
					
				self.page_view.action_result = action_result
				self.page_view.blobs = blobs
				self.current_uri = uri
			
			else:
				self.page_view.content = 'Page not found'
				self.page_view.links = dict()
				self.page_view.blobs = dict()
				self.action_result = None
				
		else:
			
			user = self.user_storage.get_user_by_uri(uri)
			host, port = uri.host_port[0], uri.host_port[1]
			
			if user:
				np = PageRequest(user, uri)
			else:
				np = PageRequest(None, uri) 
			
			resp = self.send_request(host, port, np)
			
			if resp.code_is(PAGE_RESPONSE):
				
				self.page_view.content = resp.content
				self.page_view.links = dict()
				
				for linkno, linklst in resp.links.items():
					
					self.page_view.links[linkno] = URI.from_link(linklst)
					
					self.page_view.action_result = resp.action_result
					self.page_view.blobs = resp.blobs
				
				self.current_uri = resp.uri
				self.current_ext_uri = resp.uri
			
			elif resp.code_is(PAGE_RENDER_FAILED_ERROR):
				self.page_view.content = 'Page not found'
				self.page_view.links = dict()
				self.page_view.blobs = dict()
				self.action_result = None
			
			else:
				self.page_view.content = 'Impossible error!!!'
				self.page_view.links = dict()
				self.page_view.blobs = dict()
				self.action_result = None
				