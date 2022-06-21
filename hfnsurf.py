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
			prompt = '\n{}'.format(self.client.current_uri)
		else:
			prompt = '- - no page - -'
		prompt = clrb(prompt, fg = CYAN)
		current_user = self.client.user_storage.get_user_by_uri(self.client.current_uri)
		
		if current_user:
			return '{}\n[{}] >> '.format(prompt, yellow(uuid_as_hex(current_user.uid)))
		else:
			return '{}\n[{}] >> '.format(prompt, red("guest"))
			
	def run(self):
		
		cmd = ''
		
		rawcmd = 'hfnp://0.0.0.0:0/index'
		uri = URI.from_str(rawcmd)
		
		self.client.request_page(uri)
		self.client.page_view.refresh()	
			
		request_needed = False
		
		while not cmd=='.q':
						
			rawcmd = input(self.prompt())
			
			#if not (rawcmd in ('.q','.l','.=')) and (rawcmd.replace(' ','') != ''):
			if request_needed:
					
				if self.client.current_ext_uri:
					self.client.current_ext_uri.payload = dict()
					
				if self.client.current_uri:
					self.client.current_uri.payload = dict()
							
			request_needed = False
			
			if rawcmd == '.':
				
				if self.client.current_uri.host_port == ('0.0.0.0',0):
					
					if self.client.current_ext_uri:
						
						self.client.current_uri = self.client.current_ext_uri
						request_needed = True
						
				else:
					
					self.client.current_uri = self.client.current_int_uri
					request_needed = True
				
			elif rawcmd.replace(' ','') == '':
				
				if self.client.page_view.scroll_back:
					
					if self.client.page_view.current_line > 0:
						self.client.page_view.current_line -= 1
					
				else:
					self.client.page_view.current_line += 1
					
				self.client.page_view.refresh()
				
			elif rawcmd == '/':
				
				self.client.current_uri.components = ('index',) 
				request_needed = True
					
				
			elif rawcmd == '.r':
				request_needed = True
				
			elif rawcmd == '.l':
				
				self.client.page_view.scroll_back = not self.client.page_view.scroll_back
				
				if self.client.page_view.scroll_back:
					
					if self.client.page_view.current_line > 0:
						self.client.page_view.current_line -= 1
					
				else:
					self.client.page_view.current_line += 1
					
				self.client.page_view.refresh()
				
			elif rawcmd == '.=':
				
				self.client.page_view.current_line = 0
				self.client.page_view.scroll_back = False
				
				self.client.page_view.refresh()
				
			elif rawcmd in ('?','help'):
				
				rawcmd = 'hfnp://0.0.0.0:0/help'
				self.client.current_uri = URI.from_str(rawcmd)
				request_needed = True
			
				
			elif rawcmd.startswith(':'):
				
				rawcmd = rawcmd[1:]
				
				args = shlex.shlex(rawcmd, posix=True)

				args.whitespace_split = True
				args = list(args)
				
				cmd = args.pop(0)
								
				for i, arg in enumerate(args):
					self.client.current_uri.set_payload('value{}'.format(i), arg)
					
				self.client.current_uri.set_payload('action',cmd)
				request_needed = True
				
				
			elif rawcmd in self.client.page_view.links:
					
				self.client.current_uri = self.client.page_view.links[rawcmd]
				request_needed = True
				
			elif rawcmd != '.q':
				
				if rawcmd.startswith('hfnp://'):
					
					self.client.current_uri = URI.from_str(rawcmd)
					request_needed = True
					
				elif rawcmd.startswith('/'):
					
					self.client.current_uri.components = rawcmd[1:].split('/')
					request_needed = True
				
		
			#if not (rawcmd in ('.q','.l','.=')) and (rawcmd.replace(' ','') != ''):
			if request_needed:
				
				self.client.request_page(self.client.current_uri)
				self.client.page_view.scroll_back = False 
				self.client.page_view.current_line = 0
				self.client.page_view.refresh()	
			
			elif rawcmd == '.q':
				cmd = '.q'	
				print('\nThank you for using hfnsurf.')
				
			else:
			
				self.client.page_view.refresh()	

BROWSER = Browser()
BROWSER.run()