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

###############################################################################

class PageView:
	
	
	def __init__(self, client):
		
		self.client = client
		
		self.content = ''
		
		self.links = dict()
		self.blobs = dict()
		self.action_result = None
		
		self.active = False
		
	def refresh(self):
		
		lns = len(self.content.split('\n'))
		
		sz = os.get_terminal_size()
		wh = sz.lines - lns - 5
		
		os.system('clear')		
		print(self.content)		
		
		if wh>0:
			for i in range(0, wh):
				print('')
		
		print('')
		print('-'*(sz.columns-5))
		