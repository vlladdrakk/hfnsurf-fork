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
	return '\033[31m{}\033[0m'.format(s)

def green(s):
	return '\033[32m{}\033[0m'.format(s)
	
def yellow(s):
	return '\033[93m{}\033[0m'.format(s)
		
def cyan(s):
	return '\033[96m{}\033[0m'.format(s)
	
def orange(s):
	return '\033[33m{}\033[0m'.format(s)
	
def pink(s):
	return '\033[95m{}\033[0m'.format(s)
	
def blue(s):
	return '\033[93m{}\033[0m'.format(s)

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
	return '\033[{}m\033[{}m{}\033[0m'.format(f, b, s)
	
def clrb(s, fg = WHITE, bg = BLACK):
	
	f = fg[0]
	b = bg[1]
	return '\033[1m\033[{}m\033[{}m{}\033[0m'.format(f, b, s)


def line():
	return '----------------------------------------'