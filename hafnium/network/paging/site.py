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

from .user_storage import *
from .dispatcher import *
from .rights import *
from .processors import *
from .uri import *
from .inbuilt_processor import *

###############################################################################


class HafnumPagingSite:
	
	def __init__(self, server: "HafniumPagingServer",
					quasidomain: Optional[str] = None,
					dispatcher: Optional["HafniumPageDispatcher"] = None):
		
		self.server = server
		
		self.quasidomain = quasidomain
		
		self.dispatcher = dispatcher
		
		if not dispatcher:
			self.dispatcher = HafniumPageDispatcher(self)
			
		self.user_storage = UserStorage(self)
		self.rights_storage = RightsStorage(self)

	
	def sitename(self) -> str:
		
		if self.quasidomain:
			components = self.quasidomain.split('.')[:-1]
			return '.'.join(components)

		
	def site_address(self) -> str:
		
		if self.quasidomain:
			try:
				return self.quasidomain
			except:
				return '{}:{}'.format(self.server.host, self.server.port)
		
		else:
			return '{}:{}'.format(self.server.host, self.server.port)
		