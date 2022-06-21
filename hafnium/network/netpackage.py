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

from ..package import *
from ..utility import *

###############################################################################

class NetPackage(PackageObject):

	def __init__(self, session_id, package_code):

		super().__init__()

		"""Net packages are tied to connection id (referring
		to session containing of bundled mainpipe and listener
		sockets"""

		self.set_tp_code('session_id', 10)
		self.set_tp_code('package_code', 12)

		if session_id == None:
			self.session_id = new_uuid()
			
		else:
			self.session_id = session_id

		"""Net packages have obligatory package_code. Some of them
		are reserved"""

		if package_code == None:
			self.package_code = 0
			
		else:
			self.package_code = package_code
			
	def code_is(self, package_code):
		
		return self.package_code == package_code


###################################


CREATE_SESSION_REQUEST = 1
ASSIGN_LISTENER_REQUEST = 2
GENERIC_STATUS_RESPONSE = 3
ECHO_REQUEST = 4
NO_RESPONSE_REQUIRED = 5

class CreateSessionPackage(NetPackage):

	def __init__(self):

		super().__init__(None, CREATE_SESSION_REQUEST)


class AssignListenerPackage(NetPackage):

	def __init__(self, session_id):

		super().__init__(session_id, ASSIGN_LISTENER_REQUEST)

class SuccessNetPackage(NetPackage):

	def __init__(self, session_id):

		super().__init__(session_id, GENERIC_STATUS_RESPONSE)
		self.status = 'success'

class FailureNetPackage(NetPackage):

	def __init__(self, session_id):

		super().__init__(session_id, GENERIC_STATUS_RESPONSE)
		self.status = 'failure'

class NoResponseRequired(NetPackage):

	def __init__(self, session_id):

		super().__init__(None, NO_RESPONSE_REQUIRED)
