# the terms of the GNU General Public License as published by the Free 
# Software Foundation, either version 3 of the License, or (at your option) 
# any later version.
# 
# muodata is distributed in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for 
# more details.
# 
# You should have received a copy of the GNU General Public License along 
# with muodata. If not, see <https://www.gnu.org/licenses/>. 

###############################################################################

from random import choice
from uuid import uuid4, UUID

###############################################################################

def shortuid(length, alp = 'abcdefghijklmnopqrstuvwxyz0123456789'):
	return ''.join([choice(alp) for i in range(0,length)])

def new_uuid(provided = None):
	
	if provided:
		return provided
	else:
		return uuid4().bytes
		
get_uuid = new_uuid
		
def uuid_as_hex(uid):
	
	return str(UUID(bytes=uid))
	
def uuid_from_hex(hexuid):
	
	return UUID(hexuid).bytes