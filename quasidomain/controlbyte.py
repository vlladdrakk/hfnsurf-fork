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



class ControlByte:
	
	
	IP_SCENARIO = 0
	TLD_SCENARIO = 1
	HOSTNAME_SCENARIO = 2
	POSTFIX_SCENARIO = 3
	
	PORT_STANDART_1 = 0
	PORT_STANDART_2 = 1
	PORT_STANDART_RANGE = 2
	PORT_NONSTANDART = 3
	
	NAME_MIXIN = True
	NO_NAME_MIXIN = False
	
	VARIANT = 0
	
	
	@classmethod
	def from_bytes(cls, b: bytes, nextbyte: bytes):
		
		allbits = bytes_bits(b, padding = False)
		nbits = bytes_bits(nextbyte, padding = False)
		
		scenario_b = int(base_to_dec(allbits[0:2], 2))
		porttype_b = int(base_to_dec(allbits[2:4], 2))
		
		name_mixin = allbits[4]=='1'
		var_ext = allbits[5]=='1'
		
		var_b = allbits[-2:]
		
		if var_ext:
			var_b += nbits
		
		var_b = int(base_to_dec(var_b, 2))
		
		if var_ext:
			var_b += 4
					
		return ControlByte(scenario = scenario_b,
							port_type = porttype_b,
							name_mixin = name_mixin,
							variant = var_b)
	
	
	def __init__(self, scenario: int = IP_SCENARIO,
						port_type: int = PORT_STANDART_1,
						name_mixin: bool = NAME_MIXIN,
						variant: int = VARIANT):
		
		self.scenario = scenario
		self.port_type = port_type
		self.name_mixin = name_mixin
		self.variant = variant
		
		if self.scenario>3 or self.port_type>3 or self.variant>1027:
			raise ControlByteFailure
		
	def as_bytes(self) -> bytes:
		
		scenario_b = right_bits(self.scenario, 2)
		port_b = right_bits(self.port_type, 2)
		
		if self.name_mixin: nm_b = '1'
		else: nm_b = '0'
		
		techvar = self.variant-4
		
		if techvar<0:
			
			varsm_b = '0'+ right_bits(self.variant, 2)
			aux_b = '00000000'
			
		else:
			
			var_b = '1'+ right_bits(techvar, 10)
			aux_b = var_b[-8:]
			varsm_b = var_b[:-8]
		
		keybyte_val = scenario_b+port_b+nm_b+varsm_b
		keybyte_val = unsigned_int_to_bytes(int(base_to_dec(keybyte_val, 2)),bytelen=1)
		
		auxbyte_val = unsigned_int_to_bytes(int(base_to_dec(aux_b, 2)),bytelen=1)
		
		return keybyte_val, auxbyte_val