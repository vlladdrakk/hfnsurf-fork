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

from hafnium.network.paging.dispatcher import *

from modules.pages.welcome import *
from modules.pages.help import *
from modules.pages.usermanage import *

###############################################################################

class InternalDispatcher:
	
	def __init__(self, client):
		
		self.client = client
		
	def handle_uri(self, user, uri):
		
		page = None
		if uri.getpart(0) == 'welcome':
			page = BrowserWelcomePage(self.client, user, uri)
			
		if uri.getpart(0) == 'help':
			page = BrowserHelpPage(self.client, user, uri)
			
		if uri.getpart(0) == 'usermanage':
			page = UserManagePage(self.client, user, uri)
			
		if page:
			return page.generate()
			
		else:
			return None, None, None, None, None