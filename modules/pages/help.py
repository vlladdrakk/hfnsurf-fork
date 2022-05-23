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
<BGCYAN><BLACK><BLD>- - - HELP SYSTEM - - -<NORM>

At the bottom of your screen there's an URL line and a prompt.
You can issue commands using this prompt.

You can see that your URL line says <BLD>hfnp://0.0.0.0:0/help<NORM>.
Let's break it down.

<GOLD>hfnp://<NORM> is the shorthand name of the protocol that's used.

<GOLD>0.0.0.0:0<NORM> is (normally) an IP or a (quasi)domain name of a
server which you're currently browsing.

Right now, though, you're looking at your browser's internal technical 
page, and such pages are assigned a 0.0.0.0 as a pseudo-IP, and 0 as a 
pseudo-port. Don't worry about these. It's kind of like "about:config" 
in Mozilla Firefox.

<GOLD>help<NORM> is the name of the page on a server that you're browsing
right now. A server may have a lot of pages and other things.

<CYAN><BLD>Dealing with big pages<NORM>

Some pages are bigger than your terminal window (most likely, this page too).
Here's how to deal with it:

* Press <CYAN>RETURN<NORM> (that is, issue an empty command) to view 
the next portion of your page.
* Issue a <CYAN>"-"<NORM> (minus, or dash) command to view the previous portion. 
* Issue a <CYAN>"="<NORM> command to return to the beginning of the page.

<CYAN><BLD>Links<NORM>

On the pages you will see a lot of links, which look like numbers or strings
enclosed in square brackets like this: [[i::index]], [[index]].

These are links that you can follow. To follow a link, just write its label
(a number, a letter or a whole string) and press <CYAN>RETURN<NORM>. Try any of
these two links - they will both bring you back to the index page of the browser's
internal system. Then use <CYAN>"?"<NORM> or <CYAN>"help"<NORM> to return here.

<CYAN><BLD>Other commands<NORM>

* Use <CYAN><BLD>.q<NORM> to quit the browser.

* Use <CYAN><BLD>.<NORM> to switch between your last page you've visited and the
browser's internal system.

* Use <CYAN><BLD>/<NORM> to visit the index page of your current server.

* Use <CYAN><BLD>/pagename<NORM> to visit a page named "pagename" on the
current server.

* Write an entire URI, like <CYAN><BLD>hfnp://0.0.0.0:0/help<NORM> to visit that page.

* Use <CYAN><BLD>.r<NORM> to refresh the page you're currently reading.

* Use <CYAN><BLD>:actionname value0 "value1 with spaces"<NORM> to invoke an action
named "actionname" with parameters "value0" and "value1 with spaces" on the
page you're currently browsing.

"""
	
class BrowserHelpPage(InternalHFNMLPage):
	
	def __init__(self, client, user, uri):
		
		super().__init__(client, user, uri, BROWSER_HELP_PAGE)