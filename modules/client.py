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
from hafnium.network.paging.seqstage import *
from hafnium.network.paging.exceptions import *

from modules.view import *
from modules.colors import *
from modules.user_storage import *
from modules.internal_dispatcher import *
from processors.inbuilt_processor import *
from processors.seqhash_processor import *

###############################################################################

def error_template(code, msg):
	
	res = "+ + + + + + AN ERROR HAS OCCURED + + + + + +\n"
	res += "Error code: {}\n".format(code)
	res += "Error message: {}\n".format(msg)
	res += "+ + + + + + + + + + +  + + + + + + + + + + +\n"
	
	return red(res).split('\n')


class Client:
	
	debug = True
	
	def __init__(self, browser):
		
		self.browser = browser
		
		self.user_storage = UserStorage(self)
		self.page_view = PageView(self)
		
		self.internal_dispatcher = InternalDispatcher(self)
		
		self.inbuilt_processor = DefaultInbuiltClientProcessor(self)
		self.processors = {"seqhash_auth": SeqhashAuthClientProcessor()} # {name: Processor}
		
		self.current_uri = None
		self.current_ext_uri = None
		self.current_int_uri = None
		
		try:
		#if True:
			self.load_state()
		except:
			self.save_state()
		
		self.sequence_stages = {
			'c01': ClientSequenceStage('c01', 'form_handshake_request', self.inbuilt_processor, self),
			'c02': ClientSequenceStage('c02', 'finalize_handshake_request', self.inbuilt_processor, self),
			'c03': ClientSequenceStage('c03', 'postpack_handshake_request', self.inbuilt_processor, self),
			'c09': ClientSequenceStage('c09', 'preunpack_handshake_response', self.inbuilt_processor, self),
			'c10': ClientSequenceStage('c10', 'clean_handshake_response', self.inbuilt_processor, self),
			'c11': ClientSequenceStage('c11', 'form_request', self.inbuilt_processor, self),
			'c12': ClientSequenceStage('c12', 'finalize_request', self.inbuilt_processor, self),
			'c13': ClientSequenceStage('c13', 'postpack_request', self.inbuilt_processor, self),
			'c22': ClientSequenceStage('c22', 'preunpack_response', self.inbuilt_processor, self),
			'c23': ClientSequenceStage('c23', 'unpack_blobs', self.inbuilt_processor, self),
			'c24': ClientSequenceStage('c24', 'clean_response', self.inbuilt_processor, self),
		}
		
	def stage(self, code):
		
		if code in self.sequence_stages:
			return self.sequence_stages[code]
	
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
		self.load_processors_state(sv.processors)
		
		
	def save_processors_state(self):
		
		res = dict()
		for proc_name, processor in self.processors.items():
			
			res[proc_name] = processor.storage.pack()
			
		return res
		
	def load_processors_state(self, dct):
				
		for proc_name, state in dct.items():
			if proc_name in self.processors:
				self.processors[proc_name].storage.unpack(state)
				
		
	def send_netpackage(self, host, port, np):
		
		try:
			session = OneWaySocketSession(host, port)
			session.connect(host, port)
		
			np.session_id = session.session_id
			
			response = session.send_netpackage(np)
			session.mainpipe.underlying_socket.close()
		
			return response
			
		except TimeoutError:
			raise ConnectionTimeout
			
		except ConnectionRefusedError:
			raise ConnectionRefused
			
		except:
			raise
				
	def send_request(self, host, port, request):
		
		processors = [self.processors[procname] for procname in self.processors]
		
		hs_request = HandshakeRequest()
		
		hs_request = self.stage('c01').execute(processors, hs_request)
		hs_request = self.stage('c02').execute(processors, hs_request)
		hs_request = self.stage('c03').execute(processors, hs_request)
		
		resp = self.send_netpackage(host, port, hs_request)
		
		resp = self.stage('c09').execute(processors, resp)
		resp = self.stage('c10').execute(processors, resp)
		
		processors = [self.processors[procname] for procname in resp.proc_queue]
		request.set_sequence_id(resp.sequence_id)
		
		request = self.stage('c11').execute(processors, request)
		request = self.stage('c12').execute(processors, request)
		request = self.stage('c13').execute(processors, request)
		
		resp = self.send_netpackage(host, port, request)
		
		resp = self.stage('c22').execute(processors[::-1], resp)
		resp = self.stage('c23').execute(processors[::-1], resp)
		resp = self.stage('c24').execute(processors[::-1], resp)
		
		return resp
		
		
	def request_page(self, uri):
		
		try:
		#if True:
			sz = os.get_terminal_size()
			colwidth = sz.columns
			rowheight = sz.lines
			
			if uri.host_port == ('0.0.0.0', 0):
				
				user = self.user_storage.get_user_by_uri(self.current_ext_uri)
				content, links, blobs, action_result, uri = self.internal_dispatcher.handle_uri(user, uri,
																		colwidth = colwidth, rowheight = rowheight)
							
				if content:
									
					self.page_view.content = content.split('\n')
					self.page_view.links = dict()
					
					for linkno, link_uri in links.items():
						self.page_view.links[linkno] = link_uri
						
					self.page_view.action_result = action_result
					self.page_view.blobs = blobs
					self.current_uri = uri
					self.current_int_uri = uri
				
				else:
					self.page_view.content = ['Page not found']
					self.page_view.links = dict()
					self.page_view.blobs = dict()
					self.action_result = None
					
			else:
				
				user = self.user_storage.get_user_by_uri(uri)
				host, port = uri.host_port[0], uri.host_port[1]
				
				if user:
					np = PageRequest(user, uri, colwidth = colwidth, rowheight = rowheight)
				else:
					np = PageRequest(None, uri, colwidth = colwidth, rowheight = rowheight)
				
				resp = self.send_request(host, port, np)
				
				if resp.code_is(PAGE_RESPONSE):
					
					self.page_view.content = resp.content.split('\n')
					self.page_view.links = dict()
					
					for linkno, link_uri in resp.links.items():
						
						self.page_view.links[linkno] = link_uri
						
						self.page_view.action_result = resp.action_result
						self.page_view.blobs = resp.blobs
					
					self.current_uri = resp.uri
					self.current_ext_uri = resp.uri
				
				elif resp.package_code >= 6000:
					
					self.page_view.content = error_template(str(resp.package_code), resp.text)
					self.page_view.links = dict()
					self.page_view.blobs = dict()
					self.action_result = None
					self.current_uri = uri
					self.current_ext_uri = uri
				
				else:
					self.page_view.content = ['This is an impossible error. It should not have happened. You are probably a magician.']
					self.page_view.links = dict()
					self.page_view.blobs = dict()
					self.action_result = None
					self.current_uri = uri
					self.current_ext_uri = uri
				
		except GenericHafniumPagingException as e:
			
			self.page_view.content = error_template(str(e.code), e.msg)
			self.page_view.links = dict()
			self.page_view.blobs = dict()
			self.action_result = None
			self.current_uri = uri
			self.current_ext_uri = uri
		
		except Exception as e:
			
			self.page_view.content = error_template(str(UNKNOWN_CLIENT_ERROR), "An unknown client-side error has occured: {}".format(e))
			self.page_view.links = dict()
			self.page_view.blobs = dict()
			self.action_result = None
			self.current_uri = uri
			self.current_ext_uri = uri
		
		