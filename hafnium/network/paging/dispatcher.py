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
from .exceptions import *

###############################################################################



class HafniumPageDispatcher:
	
	
	def __init__(self, site: "HafniumPagingSite"):
		
		self.site = site
	
	
	@property
	def server(self) -> "HafniumPagingServer":
		return self.site.server
	
	
	def handle_uri(self, user: "SiteUser",
						uri: "URI",
						colwidth: Optional[str] = None,
						rowheight: Optional[str] = None,
						colormode: Optional[int] = None):
	
		content = ''
		links = []
		blobs = []
		action_result = []
		URI = uri
		
		return content, links, blobs, action_result, uri