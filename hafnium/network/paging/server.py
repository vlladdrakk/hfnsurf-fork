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

from typing import Optional

from .inbuilt_processor import *

from ..server import GenericServer

###############################################################################



class HafniumPagingServer(GenericServer):
	
	
	def __init__(self, host: str,
						port: int,
						router: Optional["HafniumPagingRouter"] = None):
		
		super().__init__(host, port, router = router)
		
		self.inbuilt_processor = DefaultInbuiltServerProcessor(self)
		
		self.processors = dict() 	# {name: Processor}
		self.proc_queue = [] 		# processor names in order
		
		self.sites = dict() 		# {quasidomain or None: HafniumPagingSite}
	
	
	def get_site(self, quasidomain: str) -> Optional["HafniumPagingSite"]:
		
		if quasidomain in self.sites:
			return self.sites[quasidomain] 