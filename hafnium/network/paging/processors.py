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

from typing import Callable, Any

from ...package import *

###############################################################################



class HafniumPagingProcessor(object):
	
	
	def __init__(self, name: str):
		
		self.name = name
		self.storage = PackageObject()
		
		
	def get_stage_func(self, code: str) -> Callable:
		
		func_name = 'stage_{}'.format(code)
		
		if hasattr(self, func_name):
			return getattr(self, func_name)
			
			
			
class ClientProcessor(object):
	
	
	def __init__(self):
		
		pass
		
	def stage_c01(self, value): return value
	def stage_c02(self, value): return value
	def stage_c03(self, value): return value
	def stage_c09(self, value): return value
	def stage_c10(self, value): return value
	def stage_c11(self, value): return value
	def stage_c12(self, value): return value
	def stage_c13(self, value): return value
	def stage_c22(self, value): return value
	def stage_c23(self, value): return value
	def stage_c24(self, value): return value
			
	
	
class ServerProcessor(object):
	
	
	def __init__(self):
		
		pass
		
	def stage_s04(self, value): return value
	def stage_s05(self, value): return value
	def stage_s06(self, value): return value
	def stage_s07(self, value): return value
	def stage_s08(self, value): return value
	def stage_s14(self, value): return value
	def stage_s15(self, value): return value
	def stage_s16(self, value): return value
	def stage_s17(self, value): return value
	def stage_s18(self, value): return value
	def stage_s19(self, value): return value
	def stage_s20(self, value): return value
	def stage_s21(self, value): return value
	
	
	
class InbuiltHafniumPagingProcessor(HafniumPagingProcessor):
	
	
	def __init__(self, name: str):
		
		super().__init__(name)
		
		
	def get_stage_func(self, code: str,
						preprocess: bool = False) -> Callable:
		
		if preprocess:
			func_name = 'stage_{}_preprocess'.format(code)
		else:
			func_name = 'stage_{}'.format(code)
			
		if hasattr(self, func_name):
			return getattr(self, func_name)
			
			

class InbuiltClientProcessor(InbuiltHafniumPagingProcessor, ClientProcessor):
	
	
	def __init__(self, name: str,
						client: Any):
		
		InbuiltHafniumPagingProcessor.__init__(self, name)
		ClientProcessor.__init__(self)
		
		self.client = client
		
		
	def stage_c01_preprocess(self, value): return value
	def stage_c02_preprocess(self, value): return value
	def stage_c03_preprocess(self, value): return value
	def stage_c09_preprocess(self, value): return value
	def stage_c10_preprocess(self, value): return value
	def stage_c11_preprocess(self, value): return value
	def stage_c12_preprocess(self, value): return value
	def stage_c13_preprocess(self, value): return value
	def stage_c22_preprocess(self, value): return value
	def stage_c23_preprocess(self, value): return value
	def stage_c24_preprocess(self, value): return value
			
			

class InbuiltServerProcessor(InbuiltHafniumPagingProcessor, ServerProcessor):
	
	
	def __init__(self, name: str,
						server: "HafniumPagingerver"):
		
		InbuiltHafniumPagingProcessor.__init__(self, name)
		ServerProcessor.__init__(self)
		
		self.server = server
		
		
	def stage_s04_preprocess(self, value): return value
	def stage_s05_preprocess(self, value): return value
	def stage_s06_preprocess(self, value): return value
	def stage_s07_preprocess(self, value): return value
	def stage_s08_preprocess(self, value): return value
	def stage_s14_preprocess(self, value): return value
	def stage_s15_preprocess(self, value): return value
	def stage_s16_preprocess(self, value): return value
	def stage_s17_preprocess(self, value): return value
	def stage_s18_preprocess(self, value): return value
	def stage_s19_preprocess(self, value): return value
	def stage_s20_preprocess(self, value): return value
	def stage_s21_preprocess(self, value): return value
	
	
	
class ExternalClientProcessor(HafniumPagingProcessor, ClientProcessor):
	
	
	def __init__(self, name: str):
		
		HafniumPagingProcessor.__init__(self, name)
		ClientProcessor.__init__(self)
		
		
		
class ExternalServerProcessor(HafniumPagingProcessor, ServerProcessor):
	
	
	def __init__(self, name: str):
		
		HafniumPagingProcessor.__init__(self, name)
		ServerProcessor.__init__(self)
		
		