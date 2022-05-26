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

from muodata.uid import *

from hafnium.network.paging.processors import *
from hafnium.network.paging.netpackages import *
from hafnium.network.paging.exceptions import *

###############################################################################

	
class DefaultInbuiltClientProcessor(InbuiltClientProcessor):
	
	def __init__(self, client):
		
		super().__init__('inbuilt', client)
		
		self.storage.sequence_data = dict() # {sequence_id: data}
		
	def stage_c01_preprocess(self, value):
	
		sequence_id = new_uuid()
		value.set_sequence_id(sequence_id)
		
		return value

		