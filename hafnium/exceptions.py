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

class TypeMismatch(Exception):

    def __init__(self, expected_type, caught_type):
        super().__init__('Type mismatch during byte conversion. '+
			'Expected: {}, got {} instead.'.format(str(expected_type),
										  str(caught_type)))

class MemberTypeUnknown(Exception):

    def __init__(self):
        super().__init__('A member of the given value has an unknown type.')

class WrongElementName(Exception):

    def __init__(self):
        super().__init__('Wrong element name supplied')

class HashMismatch(Exception):

    def __init__(self):
        super().__init__('Hash mismatch')

class PackageLengthMismatch(Exception):
	
    def __init__(self):
        super().__init__('Package length mismatch')

class ByteCoderNotFoundException(Exception):
	
    def __init__(self):
        super().__init__('Bytecoder not found')

class ElementPackFailure(Exception):
	
    def __init__(self):
        super().__init__('Element packing failed')

class ElementUnpackFailure(Exception):
	
    def __init__(self):
        super().__init__('Element unpacking failed')
	
class PackFailure(Exception):
	
    def __init__(self):
        super().__init__('Package packing failed')

class UnpackFailure(Exception):
	
    def __init__(self):
        super().__init__('Package unpacking failed')

class DataTransferFailure(Exception):
	
    def __init__(self):
        super().__init__('Failed to send data via server session transport.')

class SessionIDNotProvided(Exception):
	
    def __init__(self):
        super().__init__('Session ID not provided by the netpackage.')

class SessionDoesNotExist(Exception):
	
    def __init__(self):
        super().__init__('Requested session does not exist.')

class ByteCoderToBytesFailure(Exception):
	
    def __init__(self):
        super().__init__('Bytecoder failed during conversion to bytes')

class ByteCoderFromBytesFailure(Exception):
	
    def __init__(self):
        super().__init__('Bytecoder failed during conversion from bytes')

class SocketTransferFailure(Exception):
	
    def __init__(self):
        super().__init__('Failed to send data via socket session.')
