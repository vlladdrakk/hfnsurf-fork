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
[bg=cyan][fg=256:0][b]- - - MENU - - -[/norm]
`
`[fg=red][lnk=hfnp://hafnium.nPxMa1ziTfw$/index][/lnk][/norm] MAIN PAGE OFFLINE
`[fg=green][b][lnk=help][/lnk][/norm] HELP

[case=ISPAGE]
`	[fg=green][b][lnk=usermanage][/lnk][/norm] USER MANAGEMENT
[/case]

`
`[bg=cyan][fg=256:0][b]- - -WELCOME TO HAFNIUM PAGING! - - -[/norm]
`
`HFNSurf is a Hafnium Paging Protocol browser.
`
`Type [u][fg=yellow][b]"?"[/fg] or [fg=yellow]"help"[/norm] and press ENTER
`to see a quick tutorial.
`

`[fg=green]-------------------------------------------
`Visit Hafnium Paging Protocol hfnsite here:[/norm]
`	   > > > > [b][bg=yellow][fg=256:0][lnk=hfnp://hafnium.D4GREATu/index]h[/lnk][/norm] < < < <
`[fg=green]-------------------------------------------[/norm]

"""


class BrowserWelcomePage(InternalHFNMLPage):
	
	def __init__(self, client, user, uri):
		
		super().__init__(client, user, uri, BROWSER_WELCOME_PAGE)
		
	def generate_page(self):
		
		self.set_field("ISPAGE", True)
		
		if self.client.current_ext_uri == None:
			self.set_field("ISPAGE", False)
			
		self.set_field('URI', str(self.client.current_ext_uri))
		