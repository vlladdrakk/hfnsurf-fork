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
from .processors import *
from .netpackages import *
from .exceptions import *

###############################################################################

	
	
class SeqhashAuthServerProcessor(ExternalServerProcessor):
	
	
	def __init__(self):
		
		super().__init__('seqhash_auth')
		
		self.storage.sequence_data = dict() # {sequence_id: data}
		self.storage.user_secrets = dict() # {user_id: secret}
		self.storage.user_secrets_to_send = dict() # {sequence_id: secret}
		
		
	def stage_s07(self, value: "NetPackage") -> "NetPackage": 
		# SENDING A NONCE TO THE CLIENT
		
		seqnonce = randbytes(32)
		value.seqnonce = seqnonce
		self.storage.sequence_data[value.sequence_id] = seqnonce
	
		return value
			
			
	def stage_s15(self, value: "NetPackage") -> "NetPackage": 
		# CHECKING IF THE RECEIVED SEQHASH IS CORRECT	
		
		if value.has_element('uid') and value.uid and (not value.code_is(ADD_USER_REQUEST)):
			
			if not value.uid in self.storage.user_secrets:
				raise UserNotFound
				
			user_secret = self.storage.user_secrets[value.uid]
			seqhash = value.seqhash
			seqnonce = self.storage.sequence_data.pop(value.sequence_id)
			
			hasher = hashlib.sha256()
			hasher.update(user_secret+seqnonce)
			check_seqhash = hasher.digest()
						
			if check_seqhash != seqhash:
				raise AccessDeniedError("Invalid seqhash in seqhash authentication processor.")
				
		if value.has_element('uid') and value.uid and value.code_is(ADD_USER_REQUEST):
			
			user_secret = randbytes(32)
			self.storage.user_secrets[value.uid] = user_secret
			self.storage.user_secrets_to_send[value.sequence_id] = user_secret
			
		if value.has_element('uid') and value.uid and value.code_is(REMOVE_USER_REQUEST):
			
			if value.uid in self.storage.user_secrets:
				del self.storage.user_secrets[value.uid]
				
			else:
				raise UserNotFound
			
		return value
		
			
	def stage_s19(self, value: "NetPackage") -> "NetPackage": 
		# SENDING USER'S SECRET ONCE
		
		if value.sequence_id in self.storage.user_secrets_to_send:
			value.new_seqhash_user_secret = self.storage.user_secrets_to_send.pop(value.sequence_id)
		
		return value
		