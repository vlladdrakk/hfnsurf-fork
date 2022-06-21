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

from muodata.uid import *
from muodata.binary import *

from ..netpackage import *

###############################################################################



class HafniumPagingNetPackage(NetPackage):
	
	
	def __init__(self, package_code: str):
		
		super().__init__(None, package_code)
		
		
	def set_sequence_id(self, sequence_id: bytes):
		
		self.sequence_id = sequence_id
		
		

"""
" REQUESTS
"""

HANDSHAKE_REQUEST = 4200
ADD_USER_REQUEST = 4201
REMOVE_USER_REQUEST = 4202
PAGE_REQUEST = 4203



class HandshakeRequest(HafniumPagingNetPackage):
	
	
	def __init__(self):
		
		super().__init__(HANDSHAKE_REQUEST)
		
		
		
class AddUserRequest(HafniumPagingNetPackage):
	
	
	def __init__(self, uid: Optional[bytes],
						uri: "URI"):
		
		super().__init__(ADD_USER_REQUEST)
		
		self.uid = uid
		self.uri = uri



class RemoveUserRequest(HafniumPagingNetPackage):
	
	
	def __init__(self, uid: Optional[bytes],
						uri: "URI"):
		
		super().__init__(REMOVE_USER_REQUEST)
		
		self.uid = uid
		self.uri = uri



class PageRequest(HafniumPagingNetPackage):
	
	
	def __init__(self, user: Optional["User"],
						uri: "URI",
						colwidth: Optional[int] = None,
						rowheight: Optional[int] = None,
						colormode: Optional[int] = None):
		
		super().__init__(PAGE_REQUEST)
		
		if user:
			self.uid = user.uid
		else:
			self.uid = None
	
		self.uri = uri
		
		self.colwidth = colwidth
		self.rowheight = rowheight
		
		self.colormode = colormode


"""
" RESPONSES
"""

HANDSHAKE_RESPONSE = 5200
USER_ADDED_RESPONSE = 5201
GENERAL_SUCCESS_RESPONSE = 5202
PAGE_RESPONSE = 5203



class HandshakeResponse(HafniumPagingNetPackage):


	def __init__(self, proc_queue: list[str],
						sequence_data: dict):
		
		super().__init__(HANDSHAKE_RESPONSE)
		
		self.proc_queue = proc_queue
		self.sequence_data = sequence_data



class UserAddedResponse(HafniumPagingNetPackage):
	
	
	def __init__(self):
		
		super().__init__(USER_ADDED_RESPONSE)
		self.status = 'added'
		
		
		
class GeneralSuccessResponse(HafniumPagingNetPackage):
	
	
	def __init__(self):
		
		super().__init__(GENERAL_SUCCESS_RESPONSE)
		
		self.status = 'success'
		
		
		
class PageResponse(HafniumPagingNetPackage):
	
	
	def __init__(self, content: str,
						links: dict[str, "URI"], 
						blobs: dict[str, bytes],
						action_result: list[str],
						uri: "URI"):
		
		super().__init__(PAGE_RESPONSE)
		
		self.content = content
		self.links = links
		self.blobs = blobs
		self.action_result = action_result
		self.uri = uri


"""
" ERRORS
"""
		
class ErrorResponse(HafniumPagingNetPackage):
	
	
	def __init__(self, error_code: int,
						text: str):
		
		super().__init__(error_code)
		self.text = text