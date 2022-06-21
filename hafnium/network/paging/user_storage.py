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

from .user import *
from .exceptions import *
	
###############################################################################

	
	
class UserStorage:
	
	
	def __init__(self, site: "HafniumPagingSite"):
		
		self.site = site
		self.users = dict() # {uid: User}	
		
		
	@property
	def server(self) -> "HafniumPagingServer":
		
		return self.site.server
		
		
	def user_by_uid(self, uid: bytes) -> SiteUser:
		
		if uid and (uid in self.users):
			return self.users[uid]
			
		raise UserNotFound
			
			
	def user_by_uid_or_guest(self, uid: bytes) -> SiteUser:
		
		if uid and (uid in self.users):
			return self.users[uid]
		
		else:
			return GuestUser(self.site)
		
		
	def add_user(self, uid: bytes) -> SiteUser:
		
		if uid in self.users:
			raise UserAlreadyExists
			
		else:
			
			first_user = (len(self.users)==0)
			user = SiteUser(self.site, uid = uid)
			
			self.users[uid] = user
			
			if first_user:
				user.set_right('admin')
			
			return user
			
			
	def remove_user(self, uid: bytes) -> None:
		
		if uid in self.users:
			del self.users[uid]
		
		else:
			raise UserNotFound
			