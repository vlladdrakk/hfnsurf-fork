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

import os

from modules.colors import *

###############################################################################

class PageView:
	
	
	def __init__(self, client):
		
		self.client = client
		
		self.content = []
		
		self.links = dict()
		self.blobs = dict()
		self.action_result = None
		
		self.active = False
		
		self.current_line = 0
		
		self.scroll_back = False
		
	def refresh(self):
		
		sz = os.get_terminal_size()
		wh = sz.lines - 5
		
		startline = min(len(self.content),self.current_line)
		endline = min(len(self.content),(self.current_line+wh))
		
		portion = self.content[startline:endline]
		
		if len(portion)==0 and self.current_line > 0 and len(self.content)>0:
			self.current_line -= 1
			self.refresh()
			return
				
		os.system('clear')
		wh -= len(portion)
		
		print('\n'.join(portion))
		
		if wh>0:
			for i in range(0, wh):
				print('')
		
		print('')
		totalscr = len(self.content)
		
		if len(self.content) > 0:
			scroll = int((self.current_line / len(self.content)) * 100)
		else:
			scroll = 100
		indicator = f'{scroll}%'
		#print(clr('<< MINUS'+'---'+scroll+'-'*(sz.columns-25-len(scroll))+'RETURN >>',fg=BLACK,bg=PURPLE))
		
		if self.scroll_back:
			print(clr(f'BCK-(".l" to scroll forward, ".=" to jump to start)-{"-"*(sz.columns-59-len(indicator))}-{indicator}-',fg=BLACK,bg=PURPLE))
		else:
			print(clr(f'FWD-(".l" to scroll back, ".=" to jump to start)----{"-"*(sz.columns-59-len(indicator))}-{indicator}-',fg=BLACK,bg=PURPLE))
		
		
	def refresh_old(self):
		
		sz = os.get_terminal_size()
		wh = sz.lines - 5
		
		startline = min(len(self.content),self.current_portion*wh)
		endline = min(len(self.content),(self.current_portion+1)*wh)
		
		startline = int(self.current_portion*wh)
		endline = int((self.current_portion+1)*wh)
		portion = self.content[startline:endline]
		
		if len(portion)==0 and self.current_portion > 0:
			self.current_portion -= 1
			self.refresh()
			return
				
		os.system('clear')
		wh -= len(portion)
		
		print('\n'.join(portion))
		
		if wh>0:
			for i in range(0, wh):
				print('')
		
		print('')
		totalscr = int(float(len(self.content))/(endline - startline))+1
		scroll = f'(scroll {self.current_portion+1}/{totalscr})'
		print(clr('<< MINUS'+'---'+scroll+'-'*(sz.columns-25-len(scroll))+'RETURN >>',fg=BLACK,bg=PURPLE))
		