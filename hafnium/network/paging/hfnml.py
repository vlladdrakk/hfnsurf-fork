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

from muodata.repr import *

from .page import *

###############################################################################

		
COLORS_4_BIT_FG = {
	'black':	'30',
	'red': 		'31',
	'green': 	'32',
	'yellow':	'33',
	'blue': 	'34',
	'magenta':	'35',
	'cyan': 	'36',
	'white': 	'37',
	'br_black': '90',
	'gray': 	'90',
	'br_red': 	'91',
	'br_green': '92',
	'br_yellow':'93',
	'br_blue': 	'94',
	'br_magenta':'95',
	'br_cyan': 	'96',
	'br_white': '97',
}
		
COLORS_4_BIT_BG = {
	'black':	'40',
	'red': 		'41',
	'green': 	'42',
	'yellow':	'43',
	'blue': 	'44',
	'magenta':	'45',
	'cyan': 	'46',
	'white': 	'47',
	'br_black': '100',
	'gray': 	'100',
	'br_red': 	'101',
	'br_green': '102',
	'br_yellow':'103',
	'br_blue': 	'104',
	'br_magenta':'105',
	'br_cyan': 	'106',
	'br_white': '107',
}

CENTER_MRK = chr(58359)
RIGHT_MRK = chr(58360)
FITSCREEN_MRK = chr(58361)

REPSIGN = chr(58400)


def uncolor(s: str) -> [str, str, list[str]]:
	
	codes = []
	res,ressigns,code = '','',''
		
	for l in s:
		
		if l=='\033':
			code = l
			
		elif code!='' and l=='m':
			code += 'm'
			codes.append(code)
			code = ''
			ressigns += REPSIGN
			
		elif code == '':
			res += l
			ressigns += l
			
		else:
			code += l
						
	return res, ressigns, codes
	
	
def ucj(cs: str, i: int) -> str:
	
	if i == None: return cs
	
	s, _, _ = uncolor(cs)
	
	l = i - len(s)
	leftpad = int(l/2.0)
	rightpad = l - leftpad
	
	if rightpad<0: rightpad = 0
	if leftpad<0: leftpad = 0
	
	return "{}{}{}".format(' '*leftpad, cs, ' '*rightpad)
	

def urj(cs: str, i: int) -> str:
	
	if i == None: return cs
	s, _, _= uncolor(cs)
	
	l = i - len(s)
	
	return "{}{}".format(' '*l, cs)
	
	
def ulj(cs: str, i: int) -> str:
	
	if i == None: return cs
	s, _, _ = uncolor(cs)
	
	l = i - len(s)
	
	return "{}{}".format(cs, ' '*l)
	

def chop_width(cs: str, w: int) -> list[str]:
	
	s, ss, codes = uncolor(cs)
	
	if w == None:
		return [cs]
	
	chopped = []
	
	leftcaret = 0
	rightcaret = 0
	hold = 0
	
	while rightcaret<len(ss):
		
		if ss[rightcaret] == REPSIGN:
			hold += 1
			
		if rightcaret - leftcaret - hold == w:
			
			portion = ''
			
			for sss in ss[leftcaret:rightcaret]:
				
				if sss == REPSIGN:
					portion+=codes.pop(0)
					
				else:
					portion+=sss
			
			chopped.append(portion)
				
			hold = 0
			leftcaret = rightcaret
		
		rightcaret += 1
	
	portion = ''
			
	for sss in ss[leftcaret:]:
		
		if sss == REPSIGN:
			portion+=codes.pop(0)
			
		else:
			portion+=sss
			
	chopped.append(portion)
	
	return chopped


	
class HFNMLPage(Page):
	
	
	def __init__(self, site: "HafniumPagingSite",
						user: "SiteUser",
						uri: "URI",
						template: str):
	
		super().__init__(site, user, uri)
		self.hfnml_template = HFNMLTemplate(template, self, user)
				
				
	def generate(self,
				inherited_action_result: Optional[str] = None) -> [str,	dict[str, "URI"], dict[str, bytes], list[str], "URI"]:
		
		if not inherited_action_result:
			self.action_result = set()
			
		else:
			self.action_result = inherited_action_result
		
		action = self.uri.get_payload('action')
		
		if action:

			func_name = 'action_{}'.format(action)
			
			if hasattr(self, func_name):
				self.action_result.add(getattr(self, func_name)())
		
		if self.redirect_page:
			return self.redirect_page.generate(inherited_action_result = self.action_result)
				
		self.generate_page()		
		
		if self.redirect_page:
			return self.redirect_page.generate(inherited_action_result = self.action_result)
								
		self.hfnml_template.fill()
				
		return self.content, self.links, self.blobs, self.action_result, self.uri
		

	def set_field(self, fld: str,
						val: str) -> None:
		
		self.hfnml_template.fields[fld] = val
		
		
	def get_field(self, fld: str,
						val: str) -> None:
		
		if fld in self.hfnml_template.fields:
			return self.hfnml_template.fields[fld]
			
		return '??????'

		
		
class ParseToken:
	
	
	def __init__(self, tag: str = '',
						closed_tag: bool = None,
						text: str = '',
						attribute: str = ''):
							
		self.tag = tag
		self.closed_tag = []
		self.text = text
		self.attribute = attribute
		
		self.is_tag = False
		self.is_closing_tag = False
		self.awaiting_close = False
		self.writing_attribute = False
		
		self.imposes_ignore_text = False
		
		
	def __repr__(self) -> str:
		
		res = ''
		if self.is_tag: res = '<TAG {} ATTR {}>'.format(self.tag, self.attribute)
		if self.is_closing_tag: res = '<CLTAG {} CLOSES {}>'.format(self.tag, self.closed_tag)
		if self.text != '': res = '<TEXT {}>'.format(self.text)
		if self.imposes_ignore_text: res += '!!!'
		
		return res
	
	
	
class HFNMLTemplate:
	
	
	def __init__(self, template: str,
						page: "HafniumPagingSite",
						user: "SiteUser"):
		
		self.template = template
		self.page = page
		self.user = user
		self.fields = dict()
		
		self.inner_colwidth = page.colwidth
		
		
	def color_fg(self, colorstr: str) -> str:
		
		if colorstr in COLORS_4_BIT_FG:
			return COLORS_4_BIT_FG[colorstr]
			
		if colorstr.startswith('256:'):
			return '38;5;{}'.format(colorstr[4:])
		
		if colorstr.startswith('rgb:'):
			return '38;2;{}'.format(colorstr[4:])
			
		return '39'
		
		
	def color_bg(self, colorstr: str) -> str:
		
		if colorstr in COLORS_4_BIT_BG:
			return COLORS_4_BIT_BG[colorstr]
			
		if colorstr.startswith('256:'):
			return '48;5;{}'.format(colorstr[4:])
		
		if colorstr.startswith('rgb:'):
			return '48;2;{}'.format(colorstr[4:])
		
		return '49'
		
		
	def fill(self) -> None:
		
		T = self.template
		
		
		# PRE REPLACEMENT
		
		for fld, val in self.fields.items():
			
			fldtoken = '{{{'+fld+'}}}'
			T = T.replace(fldtoken, str(val))
			
		T = T.replace('\t','')
		T = T.replace('\n','')
		T = T.replace('`','\n')
		T = T.replace('][/lnk]','] [/lnk]')
		T = T.replace('][/hlnk]','] [/hlnk]')
				
		tokens = []
		current_token = ParseToken()
		notag = False
		
		for s in T:
			
			if notag:
				current_token.text += s
				
				if current_token.text.endswith('[/notag]'):
					current_token.text = current_token.text[:-8]
					notag = False
					
			else:
			
				if s == '=' and current_token.is_tag and (not current_token.writing_attribute):
					current_token.writing_attribute = True
					
				elif s == '/' and current_token.is_tag and current_token.awaiting_close:
					current_token.is_closing_tag = True
					current_token.awaiting_close = False
					
				elif s != '/' and current_token.is_tag and current_token.awaiting_close:
					current_token.awaiting_close = False
					current_token.tag += s
				
				elif s == '[':
					
					if current_token.text or current_token.tag:
						tokens.append(current_token)
					current_token = ParseToken()
					
					current_token.is_tag = True
					current_token.awaiting_close = True
										
				elif s == ']':
					
					if current_token.is_closing_tag:
												
						for i in range(len(tokens)-1, -1, -1):
							
							if not current_token.tag == 'norm':
								if (tokens[i].tag == current_token.tag) and (not tokens[i].is_closing_tag):
									current_token.closed_tag = [tokens[i]]
									break
							else:
								if (tokens[i].tag in ('fg','bg','b','i','u','o','s','blink','uu','fraktur')) and (not tokens[i].is_closing_tag):
									current_token.closed_tag.append(tokens[i])
									
					elif current_token.tag == 'notag':
						
						notag = True
						current_token = ParseToken()
					
					if current_token.tag != 'notag':
						
						tokens.append(current_token)
						current_token = ParseToken()
					
				elif not current_token.is_tag:
					current_token.text += s
					
				else:
					if current_token.writing_attribute:
						current_token.attribute += s
					else:
						current_token.tag += s
						
		tokens.append(current_token)
						
		tags_on = []
		
		res = []
				
		for token in tokens:
			
			if token.is_tag:
				
				if token.is_closing_tag and (token.closed_tag != []) and (token.closed_tag[0] in tags_on):
					
					for clt in token.closed_tag:
						if clt in tags_on:
							tags_on.remove(clt)
										
					if token.tag == 'b':
						res.append("\033[22m")
						
					elif token.tag == 'norm':
						res.append("\033[0m")
						
					elif token.tag == 'i':
						res.append("\033[23m")
						
					elif token.tag == 'u':
						res.append("\033[24m")
						
					elif token.tag == 'o':
						res.append("\033[55m")
						
					elif token.tag == 's':
						res.append("\033[29m")
						
					elif token.tag == 'blink':
						res.append("\033[25m")
						
					elif token.tag == 'uu':
						res.append("\033[24m")
						
					elif token.tag == 'fraktur':
						res.append("\033[10m")
						
					elif token.tag == 'fg':
						res.append("\033[39m")
						
					elif token.tag == 'bg':
						res.append("\033[49m")
						
					
				elif not token.is_closing_tag:
					
					tags_on.append(token)
				
					if token.tag == 'right':
						
						rights_to_check = token.attribute.split(';')
						
						for testright in rights_to_check:
							
							if testright.startswith('~'):
								if self.user.has_right(testright[1:]):
									token.imposes_ignore_text = True
									break
									
							else:
								if self.user.hasnt_right(testright):
									token.imposes_ignore_text = True
									break
							
					elif token.tag == 'case':
												
						cases_to_check = token.attribute.split(';')
						
						for testcase in cases_to_check:
							
							negative = False
							if testcase.startswith('~'):
								negative = True
								testcase = testcase[1:]
								
							case_works = False
							
							if (testcase in self.fields) and self.fields[testcase]:
								case_works = True
								
							if testcase in self.page.action_result:
								case_works = True
								
							if negative:
								case_works = not case_works
								
							if not case_works:
								token.imposes_ignore_text = True
								break
								
					elif token.tag == 'b':
						res.append("\033[1m")
						
					elif token.tag == 'i':
						res.append("\033[3m")
						
					elif token.tag == 'u':
						res.append("\033[4m")
						
					elif token.tag == 'o':
						res.append("\033[53m")
						
					elif token.tag == 's':
						res.append("\033[9m")
						
					elif token.tag == 'blink':
						res.append("\033[5m")
						
					elif token.tag == 'uu':
						res.append("\033[21m")
						
					elif token.tag == 'fraktur':
						res.append("\033[20m")
						
					elif token.tag == 'fg' and token.attribute:
						res.append("\033[{}m".format(self.color_fg(token.attribute)))
						
					elif token.tag == 'bg' and token.attribute:
						res.append("\033[{}m".format(self.color_bg(token.attribute)))
												
						
			elif not (True in [check_token.imposes_ignore_text for check_token in tags_on]):
					
				alignmarks = []
				
				special = False
				for tag in tags_on:
						
					if tag.tag in ('lnk','hlnk'):
						
						special = True
						if tag.attribute.startswith('hfnp://'):
							link_uri = URI.from_str(tag.attribute)
						else:
							link_uri = self.page.root_uri.append(URI.from_str(tag.attribute))
								
						label = token.text
						if label in ('', ' '): label = None
						
						pagelink = self.page.generate_link(link_uri, label = label)
						
						if tag.tag != 'hlnk':
							res.append(str(pagelink))
							
					elif tag.tag == 'center':
						alignmarks.append(CENTER_MRK)
							
					elif tag.tag == 'rightalign':
						alignmarks.append(RIGHT_MRK)
							
					elif tag.tag == 'fitscreen':
						alignmarks.append(FITSCREEN_MRK)
							
				if not special:
					
					if alignmarks:
						alignmarks = "".join(alignmarks)
					else:
						alignmarks = ''
						
					if '\n' in token.text:
						res.append(token.text.replace('\n', alignmarks+'\n')+alignmarks)
					else:
						res.append(token.text+alignmarks)
					
		T = ''.join(res)	
		res = []
		
		for ln in T.split('\n'):
			
				
			if CENTER_MRK in ln:
				
				ln = ln.replace(CENTER_MRK,'')
				ln = ln.replace(RIGHT_MRK,'')
				
				if FITSCREEN_MRK in ln:
					ln = ln.replace(FITSCREEN_MRK,'')
					
					chopped = chop_width(ln, self.page.colwidth)
						
					for lln in chopped:
						res.append(ucj(lln, self.page.colwidth))
			
				else:
					
					chopped = chop_width(ln, self.inner_colwidth)
							
					for lln in chopped:
						res.append(ucj(ucj(lln, self.inner_colwidth), self.page.colwidth))
				
			elif RIGHT_MRK in ln:
				
				ln = ln.replace(RIGHT_MRK,'')
				
				if FITSCREEN_MRK in ln:
					ln = ln.replace(FITSCREEN_MRK,'')
					
					chopped = chop_width(ln, self.page.colwidth)
							
					for lln in chopped:
						res.append(urj(lln, self.page.colwidth))
			
				else:
					
					chopped = chop_width(ln, self.inner_colwidth)
							
					for lln in chopped:
						res.append(ucj(urj(lln, self.inner_colwidth), self.page.colwidth))
					
			else:
				
				if FITSCREEN_MRK in ln:
					
					ln = ln.replace(FITSCREEN_MRK,'')
					
					chopped = chop_width(ln, self.page.colwidth)
							
					for lln in chopped:
						res.append(ulj(lln, self.page.colwidth))
			
				else:
					
					chopped = chop_width(ln, self.inner_colwidth)
							
					for lln in chopped:
						res.append(ucj(ulj(lln, self.inner_colwidth), self.page.colwidth))
					
						
		res.append("\033[0m")
		self.page.content = '\n'.join(res)
		
		# POST REPLACEMENT
		for fld, val in self.fields.items():
			
			fldtoken = '{{'+fld+'}}'
			self.page.content = self.page.content.replace(fldtoken, str(val))
			