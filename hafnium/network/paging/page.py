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

from typing import Optional

from .uri import *

###############################################################################


class Page:
	
	
	COLORMODE_4_BIT = 0
	COLORMODE_8_BIT = 1
	COLORMODE_24_BIT = 2
	
	def __init__(self, site: "HafniumPagingSite",
						user: str,
						uri: URI,
						colwidth: Optional[int] = None,
						rowheight: Optional[int] = None,
						colormode: Optional[int] = None):
		
		self.site = site
		self.user = user
		self.uri = uri
		
		self.content = ''
		self.links = dict()
		self.blobs = dict()
		self.action_result = set()
		
		self.redirect_page = None
		
		self.colwidth = None
		self.rowheight = None
		
		self.colormode = colormode
		if not colormode:
			self.colormode = Page.COLORMODE_24_BIT
		
		
	@property
	def server(self) -> "HafniumPagingServer":
		return self.site.server
		
		
	def generate_link(self, link_uri: URI,
							label: Optional[str] = None):
		
		return PageLink(self, link_uri, label = label)
		
	
	def generate(self, inherited_action_result: Optional[str] = None):
		
		if not inherited_action_result:
			self.action_result = set()
			
		else:
			self.action_result = inherited_action_result
		
		action = self.uri.get_payload('action')
		
		if action:

			func_name = 'action_{}'.format(action)
			
			if hasattr(self, func_name):
				self.set_action_result(getattr(self, func_name)())
		
		if self.redirect_page:
			return self.redirect_page.generate(inherited_action_result = self.action_result)
				
		self.generate_page()		
		
		if self.redirect_page:
			return self.redirect_page.generate(inherited_action_result = self.action_result)
								
		return self.content, self.links, self.blobs, self.action_result, self.uri
		
		
	## PUBLIC METHODS	
	
	@property
	def root_uri(self) -> URI:
		
		return URI.from_str('hfnp://{}').format(self.site.site_address())
	
				
	def generate_page(self) -> None:
		
		self.content = ''
		
		
	def action_example(self) -> Optional[str]:
		
		return 'success'
	

	def set_action_result(self, result: str) -> None:
		
		self.action_result.add(result)

		
class PageLink:
	
	def __init__(self, page: Page,
						link_uri: URI,
						label: Optional[str] = None):
		
		self.page = page
		self.link_uri = link_uri
		self.label = label
		
		self.linkno = len(self.page.links)
		self.page.links[self.linklabel] = link_uri
		
		
	@property
	def linklabel(self) -> str:
		
		if self.label:
			return self.label
	
		else:
			return str(self.linkno)
		
		
	def __str__(self) -> str:
		
		return '[{}]'.format(self.linklabel)