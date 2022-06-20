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

from muodata.repr import *
from muodata.binary import *
from muodata.hex import *
from muodata.bases import *

from .exceptions import *

###############################################################################


FIRST_STANDART_PORT = 9777
SECOND_STANDART_PORT = 9778

STANDART_RANGE_START = 9779


def ip_to_bytes(ip: str) -> bytes:
	if isinstance(ip, str) and ip.count('.') == 3:
		res = b''.join([unsigned_int_to_bytes(int(h), bytelen=1) for h in ip.split('.')])
		return res
		
	else:
		raise MalformedIPAddress
	
	
def ip_from_bytes(b: bytes) -> str:
	
	if len(b) == 4:
		return '.'.join([str(i) for i in list(b)])
		
	else:
		raise MalformedIPAddress
	
	
def port_to_bytes(port: int) -> bytes:
	
	if isinstance(port, int) and port < 65536:
	
		if port in (FIRST_STANDART_PORT, SECOND_STANDART_PORT):
			return b''
		
		elif port >= STANDART_RANGE_START and port <= STANDART_RANGE_START+255:
			return unsigned_int_to_bytes(port-STANDART_RANGE_START, bytelen=1)
			
		else:
			return unsigned_int_to_bytes(port, bytelen=2)
			
	else:
		raise InvalidPortNumber
		
		
def port_from_bytes(b: bytes) -> int:
	
	if len(b) == 1:
		return STANDART_RANGE_START + bytes_to_unsigned_int(b)
		
	elif len(b) == 2:
		return bytes_to_unsigned_int(b)
		
	else:
		raise InvalidPortNumber