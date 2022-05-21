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

from hafnium.network.paging.uri import *

###############################################################################

def red(s):
	return f'\033[31m{s}\033[0m'

def green(s):
	return f'\033[32m{s}\033[0m'
	
def yellow(s):
	return f'\033[93m{s}\033[0m'
		
def cyan(s):
	return f'\033[96m{s}\033[0m'
	
def orange(s):
	return f'\033[33m{s}\033[0m'
	
def pink(s):
	return f'\033[95m{s}\033[0m'
	
def blue(s):
	return f'\033[93m{s}\033[0m'

RED = ['31','41']
GREEN = ['32','42']
CYAN = ['36','46']
ORANGE = ['33','43']
WHITE = ['37','47']
BLACK = ['30','40']
BLUE = ['34','44']
PURPLE = ['35','45']
	
def clr(s, fg = WHITE, bg = BLACK):
	f = fg[0]
	b = bg[1]
	return f'\033[{f}m\033[{b}m{s}\033[0m'
	
def clrb(s, fg = WHITE, bg = BLACK):
	
	f = fg[0]
	b = bg[1]
	return f'\033[1m\033[{f}m\033[{b}m{s}\033[0m'


def line():
	return '----------------------------------------'