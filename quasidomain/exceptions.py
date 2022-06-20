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

class SDNEEncodingFailed(Exception):
	
	def __init__(self): super().__init__()
	
class MalformedIPAddress(Exception):
	
	def __init__(self): super().__init__()
	
class InvalidPortNumber(Exception):
	
	def __init__(self): super().__init__()
	
class ControlByteFailure(Exception):
	
	def __init__(self): super().__init__()