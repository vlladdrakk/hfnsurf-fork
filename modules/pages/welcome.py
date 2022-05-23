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

from hafnium.network.paging.page import *
from hafnium.network.paging.hfnml import *
from hafnium.network.paging.uri import *

from modules.pages.internal_template import *

###############################################################################

BROWSER_WELCOME_PAGE = \
"""
<BGCYAN><BLACK><BLD>- - - MENU - - -<NORM>

<RED>[[hfnp://hafniumpaging.tiuTdXXR/index]]<NORM> MAIN PAGE OFFLINE
<GREEN><BLD>[[help]]<NORM> HELP
ISPAGE ??? <GREEN><BLD>[[usermanage]]<NORM> USER MANAGEMENT

<BGCYAN><BLACK><BLD>- - - WELCOME TO HAFNIUM PAGING! - - -<NORM>

HFNSurf is a Hafnium Paging Protocol browser.

Type <GOLD><BLD>"?"<NORM> or <GOLD><BLD>"help"<NORM> and press ENTER
to see a quick tutorial.

<GREEN>-------------------------------------------<NORM>
<GREEN>Visit Hafnium Paging Protocol hfnsite here:<NORM>
           > > > > <BLD><BGGOLD><BLACK>[[h::hfnp://hafniumpaging.8Ig4sHZ6/index]]<NORM> < < < <
<GREEN>-------------------------------------------<NORM>

"""
	
class BrowserWelcomePage(InternalHFNMLPage):
	
	def __init__(self, client, user, uri):
		
		super().__init__(client, user, uri, BROWSER_WELCOME_PAGE)
		
	def generate_page(self):
		
		self.set_field("ISPAGE", True)
		
		if self.client.current_ext_uri == None:
			self.set_field("ISPAGE", False)
			
		self.set_field('URI', str(self.client.current_ext_uri))
		