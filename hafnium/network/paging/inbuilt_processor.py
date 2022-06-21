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

from .processors import *
from .netpackages import *
from .exceptions import *

###############################################################################

	
	
class DefaultInbuiltServerProcessor(InbuiltServerProcessor):
	
	
	def __init__(self, server: "HafniumPagingServer"):
		
		super().__init__('inbuilt', server)
		
		self.storage.sequence_data = dict() # {sequence_id: data}
		
		
	def stage_s06_preprocess(self, value: "NetPackage") -> "NetPackage":
		
		self.storage.sequence_data[value.sequence_id] = dict()
				
		sequence_data = dict()
		proc_queue = self.server.proc_queue[::-1]
		
		resp = HandshakeResponse(proc_queue, sequence_data)
		return resp
		
		
	def stage_s16_preprocess(self, value: "NetPackage") -> "NetPackage":

		value.sitename = None
		
		if value.uri.quasidomain:
			value.sitename = value.uri.quasidomain
		
		return value
			
	
	def stage_s18(self, value: "NetPackage") -> "NetPackage":

		site = self.server.get_site(value.sitename)
		
		if site:
			
			if value.code_is(ADD_USER_REQUEST):
						
				uid = value.uid
				
				result =  site.user_storage.add_user(uid)
				
				if result:
					return UserAddedResponse()
									
			elif value.code_is(REMOVE_USER_REQUEST):
						
				site.user_storage.remove_user(value.uid)
				return GeneralSuccessResponse()
						
				
			elif value.code_is(PAGE_REQUEST):
					
				user = site.user_storage.user_by_uid_or_guest(value.uid)
					
				content, links, blobs, action_result, uri = site.dispatcher.handle_uri(user,
																		value.uri,
																		colwidth = value.colwidth,
																		rowheight = value.rowheight)
						
				return PageResponse(content, links, blobs, action_result, uri)
			

		raise SiteNotFound
 
	

	