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

from hafnium.network.paging.page import *
from hafnium.network.paging.hfnml import *
from hafnium.network.paging.uri import *
from hafnium.network.paging.netpackages import *
from hafnium.network.paging.user import *

from modules.pages.internal_template import *

###############################################################################


USER_MANAGE_PAGE = \
"""
[bg=cyan][fg=256:0][b]- - - USER MANAGEMENT - - -[/norm]``
`
[bg=green][fg=256:0]
[case=ADDED]You have successfully added a user`[/case]
[case=REMOVED]You have successfully removed a user`[/case]
[/norm]
[bg=red][fg=256:0]
[case=ALREADY_EXISTS]This user UID already exists on server. Adding aborted`[/case]
[case=USER_NOT_FOUND]This user UID does not exist on server. The entry removed from storage.`[/case]
[case=UNKNOWN_ERROR]Unknown error while adding a user`[/case]
[/norm]

[case=~ISPAGE]

	[fg=red][b]You have not visited any site yet.`[/norm][/case]
	
[case=ISPAGE]
	[b]LIST OF USERS[/b]`
	[fg=cyan]This is the list of users you have registered on [/fg][fg=yellow][b]{{ADDRESS}}[/norm]``
	
	[bg=green][fg=256:0][b][lnk=usermanage?action=newuser][/lnk][/norm] Create new user`
	[bg=green][fg=256:0][b][lnk=usermanage?action=asguest][/lnk][/norm] Revert to viewing as guest``
{{{USERLIST}}}

[/case]


"""

class UserManagePage(InternalHFNMLPage):
	
	def __init__(self, client, user, uri):
		
		super().__init__(client, user, uri, USER_MANAGE_PAGE)
				
	def compile_user_list(self):
		
		userlist = []
		
		for siteuser in self.client.user_storage.yield_users_by_uri(self.client.current_ext_uri):
			isactive = '(------) '
			
			if siteuser.active:
				isactive = '[fg=yellow][b](ACTIVE)[/norm] '
			
			userlist.append('{}{} [fg=cyan]Switch: [lnk=usermanage?action=switch?value0={}][/lnk] Remove: [lnk=usermanage?action=remove?value0={}][/lnk][/norm]'.format(isactive, uuid_as_hex(siteuser.uid), uuid_as_hex(siteuser.uid), uuid_as_hex(siteuser.uid)))
		
		return '`\n'.join(userlist)
				
				
	def action_newuser(self):
			
		if self.client.current_ext_uri:
			
			hostport = self.client.current_ext_uri.host_port
			
			user = User()
		
			np = AddUserRequest(user.uid, self.client.current_ext_uri)
			resp = self.client.send_request(hostport[0], hostport[1], np)
			
			if resp.code_is(USER_ADDED_RESPONSE):
				
				self.action_result.add('ADDED')
				self.client.user_storage.add_user(hostport[0], hostport[1], user)
				
			elif resp.code_is(USER_ALREADY_EXISTS_ERROR):
				
				self.action_result.add('ALREADY_EXISTS')
				
			else:
				
				self.action_result.add('UNKNOWN_ERROR')
				
		
	def action_switch(self):
		
		hostport = self.client.current_ext_uri.host_port
		
		uid = uuid_from_hex(self.uri.payload['value0'])
		self.client.user_storage.set_user_active(hostport[0], hostport[1], uid)
		self.action_result.add('SWITCHED')
	
	
	def action_asguest(self):
		
		hostport = self.client.current_ext_uri.host_port
		
		self.client.user_storage.set_no_user_active(hostport[0], hostport[1])
		
		self.action_result.add('ASGUEST')
		
		
	def action_remove(self):
		
		if self.client.current_ext_uri:
			
			uid = uuid_from_hex(self.uri.payload['value0'])
			hostport = self.client.current_ext_uri.host_port
					
			np = RemoveUserRequest(uid, self.client.current_ext_uri)
			resp = self.client.send_request(hostport[0], hostport[1], np)
			
			if resp.code_is(GENERAL_SUCCESS_RESPONSE):
				
				self.client.user_storage.remove_user(hostport[0], hostport[1], uid)
				self.action_result.add('REMOVED')
				
			elif resp.code_is(USER_NOT_FOUND):
				
				self.client.user_storage.remove_user(hostport[0], hostport[1], uid)
				self.action_result.add('USER_NOT_FOUND')
				
			else:
				self.action_result.add('UNKNOWN_ERROR_REMOVE')
				
		
		
	def generate_page(self):
		
		self.set_field("ISPAGE", True)
		
		if self.client.current_ext_uri == None:
			self.set_field("ISPAGE", False)
			
		self.set_field('URI', str(self.client.current_ext_uri))
		
		if self.client.current_ext_uri.quasidomain:
			self.set_field('ADDRESS', self.client.current_ext_uri.quasidomain)
		else:
			self.set_field('ADDRESS', self.client.current_ext_uri.host_port_str)
			
		self.set_field('USERLIST', self.compile_user_list())