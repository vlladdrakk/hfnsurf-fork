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

DEBUG = False

def debug_print(s: str):
	
	global DEBUG
	
	if DEBUG:
		print(s)
	
def pretty_raw_package(b: bytes) -> None:
	"""
	Prints entire byte representation as a table. Bytes,
	if possible, are represented as characters.
	"""

	print('=RAW=hafnium=pck='+('='*46))
	
	for i in range(0,len(b),8):
		line = ''
		
		for j in range(0,min(8,len(b)-i)):
			
			bt = b[i+j]
			
			if (bt>32)and(bt<126):
				bt = chr(bt)
				
			else:
				bt = '/'+str(bt)
				
			line += '  '+bt.ljust(5)+'|'
			
		print (line)
		print ('-'*63)
		
	print ('='*63)