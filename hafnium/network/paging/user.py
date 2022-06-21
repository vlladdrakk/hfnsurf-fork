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

from typing import Optional, Union, Tuple

from muodata.repr import *
from muodata.bases import *
from muodata.binary import *
from muodata.uid import *

from .rights import *

###############################################################################



class User(object):
	
	
	def __init__(self, uid: Optional[bytes] = None):
		
		self.uid = new_uuid(provided = uid)
			
	
	
class SiteUser(User):
	
	
	def __init__(self, site: "HafnumPagingSite",
					uid: Optional[bytes] = None):
							
		super().__init__(uid = uid)
		
		self.site = site		
		self.rights = [] # list of right names
		
		self.set_right('registered')
		
		
	@property
	def server(self) -> "HafniumPagingServer":
		
		return self.site.server
		
		
	def set_right(self, right_name: str) -> None:
		
		if self.hasnt_right(right_name):
			
			right = self.site.rights_storage.get_right(right_name,
										create_if_not_exists = True)
			
			if right:
				
				self.rights.append(right_name)
				right.add_holder(self)
		
		
	def remove_right(self, right_name: str) -> None:
		
		if self.has_right(right_name):
			
			right = self.site.rights_storage.get_right(right_name)
										
			if right:
				
				self.rights.remove(right_name)
				right.remove_holder(self)
				
				if right.is_empty():
					self.site.rights_storage.remove_right(right_name)
			
		
	def has_right(self, right_name: str) -> bool:
		
		return right_name in self.rights
		
		
	def hasnt_right(self, right_name: str) -> bool:
		
		return not(right_name in self.rights)



class GuestUser(SiteUser):
	
	
	def __init__(self, site: "HafniumPagingSite"):
							
		super().__init__(site, uid = None)
		
		self.uid = new_uuid()
		
		self.remove_right('registered')
		self.set_right('guest')
		