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

import shlex

from hafnium.network.paging.uri import *

from muodata.uid import *

from modules.client import *
from modules.colors import *

###############################################################################

class Browser:
	
	def __init__(self):
		
		self.client = Client(self)
		
	def prompt(self):
		
		if self.client.current_uri:
			prompt = f'\n{self.client.current_uri}'
		else:
			prompt = f'- - no page - -'
		prompt = clrb(prompt, fg = CYAN)
		current_user = self.client.user_storage.get_user_by_uri(self.client.current_uri)
		
		if current_user:
			return f'{prompt}\n[{yellow(uuid_as_hex(current_user.uid))}] >> '
		else:
			return f'{prompt}\n[{red("guest")}] >> '
			
	def run(self):
		
		cmd = ''
		
		rawcmd = f'hfnp://0.0.0.0:0/index'
		uri = URI.from_str(rawcmd)
		
		self.client.request_page(uri)
		self.client.page_view.refresh()		
		
		while not cmd=='.q':
						
			rawcmd = input(self.prompt())
			
			if not (rawcmd in ('.q','-','=')) and (rawcmd.replace(' ','') != ''):
				
				if self.client.current_ext_uri:
					self.client.current_ext_uri.payload = dict()
					
				if self.client.current_uri:
					self.client.current_uri.payload = dict()
							
			if rawcmd == '.':
				
				if self.client.current_uri.host_port == ('0.0.0.0',0):
					if self.client.current_ext_uri:
						self.client.current_uri = self.client.current_ext_uri
				else:
					self.client.current_uri = self.client.current_int_uri
				
			elif rawcmd.replace(' ','') == '':
				
				self.client.page_view.current_portion += 1
				self.client.page_view.refresh()
				
			elif rawcmd == '/':
				self.client.current_uri.components = ('index',) 
					
				
			elif rawcmd == '.r':
				pass
				
			elif rawcmd == '-':
				
				if self.client.page_view.current_portion > 0:
					self.client.page_view.current_portion -= 1

				self.client.page_view.refresh()
				
			elif rawcmd == '=':
				
				self.client.page_view.current_portion = 0

				self.client.page_view.refresh()
				
			elif rawcmd in ('?','help'):
				
				rawcmd = f'hfnp://0.0.0.0:0/help'
				self.client.current_uri = URI.from_str(rawcmd)
			
				
			elif rawcmd.startswith(':'):
				
				rawcmd = rawcmd[1:]
				
				args = shlex.shlex(rawcmd, posix=True)

				args.whitespace_split = True
				args = list(args)
				
				cmd = args.pop(0)
								
				for i, arg in enumerate(args):
					self.client.current_uri.set_payload(f'value{i}', arg)
					
				self.client.current_uri.set_payload('action',cmd)
				
				
			elif rawcmd in self.client.page_view.links:
					
				self.client.current_uri = self.client.page_view.links[rawcmd]
			
			elif rawcmd != '.q':
				
				if rawcmd.startswith('hfnp://'):
					self.client.current_uri = URI.from_str(rawcmd)
					
				elif rawcmd.startswith('/'):
					
					#if self.client.current_uri.host_port == ('0.0.0.0',0):
					#	rawcmd = f'hfnp://0.0.0.0:0/{rawcmd[1:]}'
					#	self.client.current_uri = URI.from_str(rawcmd)
					#else:
					self.client.current_uri.components = rawcmd[1:].split('/')
				
		
			if not (rawcmd in ('.q','-','=')) and (rawcmd.replace(' ','') != ''):
				self.client.request_page(self.client.current_uri)
				
				self.client.page_view.current_portion = 0
				self.client.page_view.refresh()	
			
			elif rawcmd == '.q':
				cmd = '.q'	
				print('\nThank you for using hfnsurf.')
			

BROWSER = Browser()
BROWSER.run()