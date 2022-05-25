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

BROWSER_HELP_PAGE = \
"""
[bg=cyan][fg=256:0][b]- - - HELP SYSTEM - - -[/norm]``

At the bottom of your screen there's an URL line and a prompt.
You can issue commands using this prompt.``

You can see that your URL line says [b]hfnp://0.0.0.0:0/help[/b].`
Let's break it down.``

[fg=yellow]hfnp://[/fg] is the shorthand name of the protocol that's used.``

[fg=yellow]0.0.0.0:0[/fg] is (normally) an IP or a (quasi)domain name of a
server which you're currently browsing.``

Right now, though, you're looking at your browser's internal technical `
page, and such pages are assigned a 0.0.0.0 as a pseudo-IP, and 0 as a `
pseudo-port. Don't worry about these. It's kind of like "about:config" `
in Mozilla Firefox.``

[fg=yellow]help[/fg] is the name of the page on a server that you're browsing`
right now. A server may have a lot of pages and other things.``

[fg=cyan][b]Dealing with big pages[/norm]``

Some pages are bigger than your terminal window (most likely, this page too).`
Here's how to deal with it:``

* Press [fg=cyan]RETURN[/fg] (that is, issue an empty command) to view `
the next portion of your page.`
* Issue a [fg=cyan]"-"[/fg] (minus, or dash) command to view the previous portion. `
* Issue a [fg=cyan]"="[/fg] command to return to the beginning of the page.``

[fg=cyan][b]Links[/norm]``

On the pages you will see a lot of links, which look like numbers or strings`
enclosed in square brackets like this: [lnk=index]i[/lnk], [lnk=index][/lnk].``

These are links that you can follow. To follow a link, just write its label`
(a number, a letter or a whole string) and press [fg=cyan]RETURN[/fg]. Try any of`
these two links - they will both bring you back to the index page of the browser's`
internal system. Then use [fg=cyan]"?"[/fg] or [fg=cyan]"help"[/fg] to return here.``

[fg=cyan][b]Other commands[/norm]`

* Use [fg=cyan][b].q[/norm] to quit the browser.`

* Use [fg=cyan][b].[/norm] to switch between your last page you've visited and the`
browser's internal system.``

* Use [fg=cyan][b]/[/norm] to visit the index page of your current server.`

* Use [fg=cyan][b]/pagename[/norm] to visit a page named "pagename" on the`
current server.``

* Write an entire URI, like [fg=cyan][b]hfnp://0.0.0.0:0/help[/norm] to visit that page.``

* Use [fg=cyan][b].r[/norm] to refresh the page you're currently reading.``

* Use [fg=cyan][b]:actionname value0 "value1 with spaces"[/norm] to invoke an action`
named "actionname" with parameters "value0" and "value1 with spaces" on the`
page you're currently browsing.``

"""
	
class BrowserHelpPage(InternalHFNMLPage):
	
	def __init__(self, client, user, uri):
		
		super().__init__(client, user, uri, BROWSER_HELP_PAGE)