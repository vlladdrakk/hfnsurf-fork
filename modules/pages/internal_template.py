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

from version import __version__

###########################################################################


INTERNAL_PAGE_TEMPLATE = """-----------------------------------------------------------------------`
`
[b]HFNSurf Browser v.VERSION Internal page system[/b]``
[fg=cyan][b][lnk=index]i[/lnk] Index page[/norm]`

[case=ISPAGE]
	[bg=yellow][fg=black][b][lnk={{{URI}}}]l[/lnk][/norm] Last visited page`
[/case]

-----------------------------------------------------------------------`
<PAGE>
"""

class InternalHFNMLPage(HFNMLPage):
	
	def __init__(self, client, user, uri, template):
		
		self.client = client
		template = INTERNAL_PAGE_TEMPLATE.replace('VERSION',__version__).replace('<PAGE>',template)
		
		super().__init__(None, user, uri, template)
	
	@property	
	def root_uri(self):
		
		return URI.from_str('hfnp://0.0.0.0:0')
	