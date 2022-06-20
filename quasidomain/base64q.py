# Copyright (c) 2022 Keith Aprilnight
# 
# This file is part of quasidomain and is licenced under the terms of MIT License.
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

import base64

###############################################################################


ALTCHARS = b'+%'


REPLACEMENTS = {
	'==': '&',
	'=': '$',
	'0': '#',
	'I': '@',
	'O': '<',
	'l': '!'
}


def b64q_encode(b: bytes,
				replacements: dict[str, str] = REPLACEMENTS,
				altchars: bytes = ALTCHARS) -> str:
	
	res = base64.b64encode(b, altchars = altchars).decode('utf-8')
	
	for rem, repl in replacements.items():
		res = res.replace(rem, repl)
		
	return res
	
	
def b64q_decode(s: str,
				replacements: dict[str, str] = REPLACEMENTS,
				altchars: bytes = ALTCHARS) -> bytes:
	
	for rem, repl in replacements.items():
		s = s.replace(repl, rem)
	
	res = base64.b64decode(s.encode('utf-8'), altchars = altchars)
	
	return res
	