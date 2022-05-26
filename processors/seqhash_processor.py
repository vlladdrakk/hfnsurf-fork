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

import hashlib

from muodata.binary import *
from hafnium.network.paging.processors import *
from hafnium.network.paging.netpackages import *
from hafnium.network.paging.exceptions import *

###############################################################################

	
class SeqhashAuthClientProcessor(ExternalClientProcessor):
	
	def __init__(self):
		
		super().__init__('seqhash_auth')
		self.storage.sequence_data = dict() # {sequence_id: data}
		self.storage.sequence_users = dict() # {sequence_id: user_uid}
		self.storage.user_secrets = dict() # {user_id: secret}
		
	def stage_c10(self, value):
		
		seqnonce = value.seqnonce
		self.storage.sequence_data[value.sequence_id] = seqnonce
		
		return value
		
		
	def stage_c13(self, value):
		
		self.storage.sequence_users[value.sequence_id] = value.uid
		
		if value.has_element('uid') and value.uid and (not value.code_is(ADD_USER_REQUEST)):
			
			seqnonce = self.storage.sequence_data.pop(value.sequence_id)
			user_secret = self.storage.user_secrets[value.uid]
			
			hasher = hashlib.sha256()
			hasher.update(user_secret+seqnonce)
			value.seqhash = hasher.digest()
		
		return value
		
	def stage_c24(self, value):
		
		
		if value.has_element('sequence_id') and (value.sequence_id in self.storage.sequence_users):
			user_uid = self.storage.sequence_users.pop(value.sequence_id)
	
		if value.has_element("new_seqhash_user_secret"):
			self.storage.user_secrets[user_uid] = value.new_seqhash_user_secret
							
		return value