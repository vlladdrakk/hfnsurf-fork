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
<BGCYAN><BLACK><BLD>- - - USER MANAGEMENT - - -<NORM>
ADDED $$$ <BGGREEN><BLACK>You have successfully added a user<NORM>
REMOVED $$$ <BGGREEN><BLACK>You have successfully removed a user<NORM>
ALREADY_EXISTS $$$ <BGRED>This user UID already exists on server. Adding aborted<NORM>
USER_NOT_FOUND $$$ <BGRED>This user UID does not exist on server. The entry removed from storage.<NORM>
UNKNOWN_ERROR $$$ <BGRED>Unknown error while adding a user.<NORM>
UNKNOWN_ERROR_REMOVE $$$ <BGRED>Unknown error while removing a user.<NORM>

ISPAGE !??? <RED><BLD>You have not visited any site yet.<NORM>

ISPAGE ??? <BLD>LIST OF USERS<NORM>
ISPAGE ??? <CYAN>This is the list of users you have registered on <NORM><GOLD><BLD>{{ADDRESS}}<NORM>

ISPAGE ??? <BGGREEN><BLACK><BLD>[[usermanage?action=newuser]]<NORM> Create new user
{{{USERLIST}}}

"""
	
class UserManagePage(InternalHFNMLPage):
	
	def __init__(self, client, user, uri):
		
		super().__init__(client, user, uri, USER_MANAGE_PAGE)
				
	def compile_user_list(self):
		
		userlist = []
		
		for siteuser in self.client.user_storage.yield_users_by_uri(self.client.current_ext_uri):
			isactive = '(------) '
			
			if siteuser.active:
				isactive = '<GOLD><BLD>(ACTIVE)<NORM> '
			
			userlist.append(f'{isactive}{uuid_as_hex(siteuser.uid)} <CYAN>Switch: [[usermanage?action=switch?value0={uuid_as_hex(siteuser.uid)}]] Remove: [[usermanage?action=remove?value0={uuid_as_hex(siteuser.uid)}]]<NORM>')
		
		return '\n'.join(userlist)
				
				
	def action_newuser(self):
			
		if self.client.current_ext_uri:
			
			hostport = self.client.current_ext_uri.host_port
			
			user = User()
		
			np = AddUserRequest(user.uid)
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
	
	def action_remove(self):
		
		if self.client.current_ext_uri:
			
			uid = uuid_from_hex(self.uri.payload['value0'])
			hostport = self.client.current_ext_uri.host_port
					
			np = RemoveUserRequest(uid)
			resp = self.client.send_request(hostport[0], hostport[1], np)
			
			if resp.code_is(GENERAL_SUCCESS_RESPONSE):
				
				self.client.user_storage.remove_user(hostport[0], hostport[1], uid)
				self.action_result.add('REMOVED')
				
			elif resp.code_is(USER_NOT_FOUND_ERROR):
				
				self.client.user_storage.remove_user(hostport[0], hostport[1], uid)
				self.action_result.add('USER_NOT_FOUND')
				
			else:
				
				self.action_result.add('UNKNOWN_ERROR_REMOVE')
				
		
		
	def generate_page(self):
		
		self.set_field("ISPAGE", True)
		
		if self.client.current_ext_uri == None:
			self.set_field("ISPAGE", False)
			
		self.set_field('URI', str(self.client.current_ext_uri))
		
		if self.client.current_ext_uri.address:
			self.set_field('ADDRESS', self.client.current_ext_uri.address)
		else:
			self.set_field('ADDRESS', self.client.current_ext_uri.host_port_str)
			
		self.set_field('USERLIST', self.compile_user_list())