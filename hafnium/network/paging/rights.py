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

###############################################################################



class UserRight(object):
	
	
	def __init__(self, name: str):
		
		self.name = name
		self.holders = dict() # {user_uid: User}
		
		
	def add_holder(self, user: "SiteUser") -> None:
		
		if not user.uid in self.holders:
			self.holders[user.uid] = user


	def remove_holder(self, user: "SiteUser") -> None:
		
		if user.uid in self.holders:		
			del self.holders[user.uid]
			
			
	def is_empty(self) -> bool:
	
		return len(self.holders) == 0

			
			
class RightsStorage(object):
	
	
	def __init__(self, site):
		
		self.site = site
		self.rights = dict() # {name: UserRight}
		
		
	@property
	def server(self) -> "HafniumPagingServer":
		return self.site.server
		
		
	def create_right(self, name: str) -> UserRight:
		
		if not name in self.rights:
			
			self.rights[name] = UserRight(name)
			return self.rights[name]
			
			
	def remove_right(self, name: str) -> bool:
		
		if name in self.rights:
			
			right = self.rights[name]
			
			if not right.is_empty():
				return False
				
			del self.rights[name]
			return True
			
		return False
		
		
	def get_right(self, name: str,
						create_if_not_exists: bool = False) -> UserRight:
		
		if name in self.rights:
			return self.rights[name]
		
		elif create_if_not_exists:
			return self.create_right(name)