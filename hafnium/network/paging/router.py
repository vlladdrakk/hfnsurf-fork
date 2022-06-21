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

from ..netpackage import *
from ..server_router import *

from .netpackages import *
from .exceptions import *
from .uri import *
from .seqstage import *

###############################################################################



class HafniumPagingRouter(HafniumServerRouter):
		

	def __init__(self, server: "HafniumPagingServer"):
		
		super().__init__(server, sessioned = False)
				
		self.sequence_stages = {
			's04': ServerSequenceStage('s04', 'preunpack_handshake_request', self.server.inbuilt_processor, self.server),
			's05': ServerSequenceStage('s05', 'clean_handshake_request', self.server.inbuilt_processor, self.server),
			's06': ServerSequenceStage('s06', 'form_handshake_response', self.server.inbuilt_processor, self.server),
			's07': ServerSequenceStage('s07', 'finalize_handshake_response', self.server.inbuilt_processor, self.server),
			's08': ServerSequenceStage('s08', 'postpack_handshake_response', self.server.inbuilt_processor, self.server),
			's14': ServerSequenceStage('s14', 'preunpack_request', self.server.inbuilt_processor, self.server),
			's15': ServerSequenceStage('s15', 'clean_request', self.server.inbuilt_processor, self.server),
			's16': ServerSequenceStage('s16', 'route_request', self.server.inbuilt_processor, self.server),
			's17': ServerSequenceStage('s17', 'dispatch_request', self.server.inbuilt_processor, self.server),
			's18': ServerSequenceStage('s18', 'form_response', self.server.inbuilt_processor, self.server),
			's19': ServerSequenceStage('s19', 'finalize_response', self.server.inbuilt_processor, self.server),
			's20': ServerSequenceStage('s20', 'pack_blobs', self.server.inbuilt_processor, self.server),
			's21': ServerSequenceStage('s21', 'postpack_response', self.server.inbuilt_processor, self.server),
		}
		
		
	def stage(self, code):
		
		if code in self.sequence_stages:
			return self.sequence_stages[code]
			
			
	def route_request(self, request: "NetPackage", 
							transport: Optional["asyncio.Transport"] = None) -> "NetPackage":
		
		try:
		#if True:
				
			try:
				session_id = request.session_id
				# debug_print(f'Routing request {request.package_code}, session_id = {byte_hex_shorthand(request.session_id)}')
				
			except:
				raise SessionIDNotFound
			
			resp = None	
			if request.package_code == CREATE_SESSION_REQUEST:
				resp = self.handle_create_session(request, session_id, transport = transport)
								
			if not resp:
				debug_print('Failed to form a response. Sending a failure request.')
				raise UnknownError
				
			return resp
		
		except GenericHafniumPagingException as e:
			return ErrorResponse(e.code, e.msg)
			
		except:
			return ErrorResponse(UNKNOWN_ERROR, "Unknown error has occured.")
		
		
	def process_request(self, raw_request: bytes,
							transport: Optional["asyncio.Transport"] = None) -> ["NetPackage", bytes]:
	
		try:
		#if True:
			
			processors = [self.server.processors[procname] for procname in self.server.proc_queue]
					
			original_request = NetPackage(None, None)
			tail = original_request.unpack(raw_request)
			
			if original_request.code_is(CREATE_SESSION_REQUEST):
				# PROCESSING LOW-LEVEL HAFNIUM REQUEST
				
				response = self.route_request(original_request, transport = transport)	
				response.session_id = original_request.session_id
				return response, tail
					
			request = self.stage('s04').execute(processors, original_request)
			request = self.stage('s05').execute(processors, request)
			
			if request.code_is(HANDSHAKE_REQUEST) and request.has_element('sequence_id'):
				# PROCESSING HANDSHAKE
				
				response = self.stage('s06').execute(processors[::-1], request)
				
				response.set_sequence_id(request.sequence_id)	
					
				response = self.stage('s07').execute(processors[::-1], response)
				response = self.stage('s08').execute(processors[::-1], response)
				
				
			else:
				
				request = self.stage('s14').execute(processors, original_request)
				request = self.stage('s15').execute(processors, request)
				
				if request.has_element('sequence_id'):
					# PROCESSING ACTUAL REQUEST
				
					request = self.stage('s16').execute(processors, request)
					request = self.stage('s17').execute(processors, request)
					response = self.stage('s18').execute(processors[::-1], request)
					
					response.set_sequence_id(request.sequence_id)	
					
					response = self.stage('s19').execute(processors[::-1], response)
					response = self.stage('s20').execute(processors[::-1], response)
					response = self.stage('s21').execute(processors[::-1], response)
				
				else:
					raise SequenceNotFound
				
			response.session_id = request.session_id
			return response, tail
		
		except GenericHafniumPagingException as e:
			
			return ErrorResponse(e.code, e.msg), tail
		
		except Exception as e:
	
			return ErrorResponse(UNKNOWN_ERROR, f"Unknown error has occured: {e}"), tail