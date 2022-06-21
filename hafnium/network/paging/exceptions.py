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



class GenericHafniumPagingException(Exception):
	
	def __init__(self, code: int, msg: str):
		
		super().__init__(code, msg)
		self.code = code
		self.msg = msg



USER_ALREADY_EXISTS = 6201
class UserAlreadyExists(GenericHafniumPagingException):
	
	def __init__(self): super().__init__(USER_ALREADY_EXISTS, "Requested user UID already exists on this site.")
	
	
	
USER_NOT_FOUND = 6202
class UserNotFound(GenericHafniumPagingException):
	
	def __init__(self): super().__init__(USER_NOT_FOUND, "Requested user UID not found on this site.")
	
	
	
PAGE_NOT_FOUND = 6203
class PageNotFound(GenericHafniumPagingException):
	
	def __init__(self): super().__init__(PAGE_NOT_FOUND, "Page not found")
	
	
	
SITE_NOT_FOUND = 6204
class SiteNotFound(GenericHafniumPagingException):
	
	def __init__(self): super().__init__(SITE_NOT_FOUND, "Site not found on this server")
	
	
	
MALFORMED_HOST = 6205
class MalformedHost(GenericHafniumPagingException):
	
	def __init__(self): super().__init__(MALFORMED_HOST, "Malformed host")
	
	
	
MALFORMED_APPENDIX = 6206
class MalformedAppendix(GenericHafniumPagingException):
	
	def __init__(self): super().__init__(MALFORMED_APPENDIX, "Malformed appendix")
	


INBUILT_PROCESSOR_UNSPECIFIED = 6207
class InbuiltProcessorUnspecified(GenericHafniumPagingException):
	
	def __init__(self): super().__init__(INBUILT_PROCESSOR_UNSPECIFIED, "In-built processor was not specified on this server")
	
	
	
SEQUENCE_NOT_FOUND = 6208
class SequenceNotFound(GenericHafniumPagingException):
	
	def __init__(self): super().__init__(SEQUENCE_NOT_FOUND, "Sequence ID not found")
	


GENERAL_PROCESSOR_ERROR = 6209
class ProcessorError(GenericHafniumPagingException):
	
	def __init__(self, msg): super().__init__(GENERAL_PROCESSOR_ERROR, msg)
	
	

ACCESS_DENIED_ERROR = 6210
class AccessDeniedError(GenericHafniumPagingException):
	
	def __init__(self, msg): super().__init__(ACCESS_DENIED_ERROR, msg)
	
	
	
UNKNOWN_CLIENT_ERROR = 6298
class UnknownClientError(GenericHafniumPagingException):
	
	def __init__(self): super().__init__(UNKNOWN_ERROR, "An unknown client-side error has occured.")
	
	

UNKNOWN_ERROR = 6299
class UnknownError(GenericHafniumPagingException):
	
	def __init__(self): super().__init__(UNKNOWN_ERROR, "An unknown error has occured.")
	
	
	
SESSION_ID_NOT_FOUND = 6211
class SessionIDNotFound(GenericHafniumPagingException):
	
	def __init__(self): super().__init__(SESSION_ID_NOT_FOUND, "Session ID not found.")
	
	
	
CONNECTION_TIMEOUT = 6213
class ConnectionTimeout(GenericHafniumPagingException):
	
	def __init__(self): super().__init__(CONNECTION_TIMEOUT, "Connection has timed out.")
	
	
	
CONNECTION_REFUSED = 6214
class ConnectionRefused(GenericHafniumPagingException):
	
	def __init__(self): super().__init__(CONNECTION_REFUSED, "Connection refused.")