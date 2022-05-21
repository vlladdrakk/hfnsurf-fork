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

from hafnium.network.paging.user import *

###############################################################################

class SiteUser:
	
	
	def __init__(self, host, port, user):
		
		self.host = host
		self.port = port
		self.user = user
		
		self.active = False

	@property
	def uid(self): return self.user.uid

class UserStorage:
	
	
	def __init__(self, client):
		
		self.client = client
		self.users = dict() # {host+port: [SiteUser]}
		
		
	def save_state(self):
		
		dct = dict()
		for hostport, siteusers in self.users.items():
		
			dct[hostport] = []
			
			for siteuser in siteusers:
				userdct = dict()
				userdct['uid'] = siteuser.uid
				userdct['active'] = siteuser.active
			
				dct[hostport].append(userdct)
				
		return dct
		
	def load_state(self, dct):
		
		self.users = dict()
		
		for hostport, siteusers in dct.items():
			
			self.users[hostport] = []
			
			for userdct in siteusers:
				
				underlying_user = User(uid = userdct['uid'])
				
				siteuser = SiteUser(hostport[0], hostport[1], underlying_user)
				siteuser.active = userdct['active']
				
				self.users[hostport].append(siteuser)
				
	def add_user(self, host, port, user):
		
		siteuser = SiteUser(host, port, user)
		host, port = str(host), int(port)
		
		if not (host, port) in self.users:
			self.users[(host, port)] = []
			
		userlst = self.users[(host, port)]
		userlst.append(siteuser)
		
		if len(userlst)==1:
			siteuser.active = True
			
		self.client.save_state()
		
		
	def get_user(self, host, port, uid):
		
		if (host, port) in self.users:
			for siteuser in self.users[(host, port)]:
				if siteuser.user.uid == uid: return siteuser
				
	def remove_user(self, host, port, uid):
		
		to_remove = None
		if (host, port) in self.users:
			for siteuser in self.users[(host, port)]:
				if siteuser.user.uid == uid:
					to_remove = siteuser
					break
			if to_remove:
				self.users[(host, port)].remove(to_remove)
			
		self.client.save_state()
								
	def get_user_by_uri(self, uri):
		
		if uri:
			hostport = uri.host_port
		
			if hostport:
				hostport = tuple(hostport)
			
				if hostport in self.users:
					for siteuser in self.users[hostport]:
						if siteuser.active: return siteuser
						
	def yield_users_by_uri(self, uri):
		
		if uri:
			hostport = uri.host_port
		
			if hostport:
				hostport = tuple(hostport)
			
				if hostport in self.users:
					
					for siteuser in self.users[hostport]:
						yield siteuser
						
	def set_user_active(self, host, port, uid):
		
		if (host, port) in self.users:
			for siteuser in self.users[(host, port)]:
				if siteuser.user.uid == uid:
					siteuser.active = True
				else:
					siteuser.active = False
			
		self.client.save_state()