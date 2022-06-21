# Copyright (c) 2022 Keith Aprilnight
# 
# This file is part of hafnium and is licenced under the terms of MIT License.
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

from typing import Any

from ..netpackage import *
from .exceptions import *

###############################################################################



class SequenceStage(object):
	
	
	def __init__(self, code: str, 
						name: str,
						inbuilt_processor: "InbuiltHafniumPagingProcessor"):
		
		self.code = code
		self.name = name
		self.inbuilt_processor = inbuilt_processor
		
		
	def execute(self, processors: list["HafniumPagingProcessor"],
						value: "NetPackage") -> "NetPackage":
		
		if self.inbuilt_processor:
			
			result_value = self.inbuilt_processor.get_stage_func(self.code,
														preprocess = True)(value)
			
			for processor in processors:
				result_value = processor.get_stage_func(self.code)(result_value)
				
			result_value = self.inbuilt_processor.get_stage_func(self.code,
														preprocess = False)(result_value)
			
			return result_value
					
		else:
			raise InbuiltProcessorUnspecified
			
			

class ClientSequenceStage(SequenceStage):
	
	
	def __init__(self, code: str,
						name: str,
						inbuilt_processor: "InbuiltClientProcessor",
						client: Any):
		
		super().__init__(code, name, inbuilt_processor)
		self.client = client
		
		
		
class ServerSequenceStage(SequenceStage):
	
	
	def __init__(self, code: str,
						name: str,
						inbuilt_processor: "InbuiltServerProcessor",
						server: "HafniumPagingServer"):
		
		super().__init__(code, name, inbuilt_processor)
		self.server = server