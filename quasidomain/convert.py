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

from typing import Optional

from muodata.repr import *
from muodata.binary import *
from muodata.hex import *
from muodata.bases import *

from .base64q import *
from .byteconv import *
from .controlbyte import *
from .sha import *
from .sdne.sdne import *
from .sdne.sdne_libs import *

###############################################################################


def calculate_appendix(scenario: int = ControlByte.IP_SCENARIO,
				ip: Optional[str] = None,
				full_hostname: str = None,
				port: int = FIRST_STANDART_PORT,
				site_name: str = None,
				name_mixin: bool = ControlByte.NAME_MIXIN,
				variant: int = ControlByte.VARIANT) -> str:
	
	if full_hostname:
		
		is_tld = True
		tld_lst = []	
		hostname = []
	
		hostnamespl = full_hostname.split('.')[::-1]
		
		for i, component in enumerate(hostnamespl):
			
			if ((component in SDNE_3) and is_tld) and i<len(hostnamespl)-1:
				tld_lst.insert(0, component)
			
			else:
				is_tld = False
				hostname.insert(0, component)
				
		hostname = '.'.join(hostname)
		
	if port == FIRST_STANDART_PORT:
		port_type = ControlByte.PORT_STANDART_1
		
	elif port == SECOND_STANDART_PORT:
		port_type = ControlByte.PORT_STANDART_2
		
	elif port >= STANDART_RANGE_START and port <= STANDART_RANGE_START+255:
		port_type = ControlByte.PORT_STANDART_RANGE
		
	else:
		port_type = ControlByte.PORT_NONSTANDART
		
	cb = ControlByte(scenario = scenario,
							port_type = port_type,
							name_mixin = name_mixin,
							variant = variant)
										
	control_byte, aux_byte = cb.as_bytes()	
	
	res = control_byte
	
	if bytes_bits(control_byte)[5] =='1':
		res += aux_byte
	
	if scenario == ControlByte.IP_SCENARIO and ip:
		
		res += port_to_bytes(port)
		res += ip_to_bytes(ip)
	
	elif scenario == ControlByte.TLD_SCENARIO and tld_lst:
		
		res += port_to_bytes(port)
		res += sdne_encode('', tld_lst=tld_lst)

	elif scenario == ControlByte.HOSTNAME_SCENARIO and hostname:
		
		res += port_to_bytes(port)
		res += sdne_encode(hostname, tld_lst=tld_lst)
		
	elif scenario == ControlByte.POSTFIX_SCENARIO and site_name.startswith(hostname):
		
		res += port_to_bytes(port)
		postfix = site_name.replace(hostname,'')
		res += sdne_encode(postfix, tld_lst=tld_lst)
		
	varhash = sha(unsigned_int_to_bytes(variant))
	res = res[:2]+bytes(intlist_bin_xor(res[2:],varhash[0:len(res)-2]))
	
	if name_mixin:
		
		sitenamehash = sha(bytes(site_name, 'utf-8'))[0:len(res)-2]
		res = res[0:1] + bytes(intlist_bin_xor(res[1:],sitenamehash))
		
	return b64q_encode(res)
	
	
def resolve_appendix(appendix: str, site_name: str) -> [str, int]:
	
	res = b64q_decode(appendix)
	
	cb = ControlByte.from_bytes(res[0:1], res[1:2])
	
	if cb.name_mixin:
		
		sitenamehash = sha(bytes(site_name, 'utf-8'))[0:len(res)-2]
		res = res[0:1] + bytes(intlist_bin_xor(res[1:],sitenamehash))
		
	cb = ControlByte.from_bytes(res[0:1], res[1:2])
	
	varhash = sha(unsigned_int_to_bytes(cb.variant))
	res = res[:2]+bytes(intlist_bin_xor(res[2:],varhash[0:len(res)-2]))
	
	if cb.variant>3:
		hostnamestartindex = 2
	else:
		hostnamestartindex = 1
	
	if cb.port_type == ControlByte.PORT_STANDART_1:
		port = FIRST_STANDART_PORT
	
	elif cb.port_type == ControlByte.PORT_STANDART_2:
		port = SECOND_STANDART_PORT
		
	elif cb.port_type == ControlByte.PORT_STANDART_RANGE:
		port = port_from_bytes(res[hostnamestartindex:hostnamestartindex+1])
		hostnamestartindex+= 1
		
	else:
		port = port_from_bytes(res[hostnamestartindex:hostnamestartindex+2])
		hostnamestartindex+=2
		
		
	if cb.scenario == ControlByte.IP_SCENARIO:
		hostname = ip_from_bytes(res[hostnamestartindex:hostnamestartindex+4])
			
	elif cb.scenario == ControlByte.TLD_SCENARIO:
		
		_, tld_lst = sdne_decode(res[hostnamestartindex:])
		hostname = site_name+'.'+'.'.join(tld_lst)

	elif cb.scenario == ControlByte.HOSTNAME_SCENARIO:
		
		hostname, tld_lst = sdne_decode(res[hostnamestartindex:])
		if tld_lst:
			hostname += '.'+'.'.join(tld_lst)
		
	elif cb.scenario == ControlByte.POSTFIX_SCENARIO:
		
		postfix, tld_lst = sdne_decode(res[hostnamestartindex:])
		
		hostname = site_name.replace(postfix,'')
		if tld_lst:
			hostname += '.'+'.'.join(tld_lst)
		
	return hostname, port