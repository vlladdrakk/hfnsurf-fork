# muodata is distributed in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for 
# more details.
# 
# You should have received a copy of the GNU General Public License along 
# with muodata. If not, see <https://www.gnu.org/licenses/>. 

###############################################################################

from pathlib import PurePosixPath, Path

from .object_tree import *


###############################################################################


class VirtualFSFile(ObjectTreeNode):

	def __init__(self, name = '', content = ''):
		
		super().__init__()
		
		self.name = name
		self.extension = ''
		
		if '.' in name:
			self.name, self.extension = name.split('.',1)
			
		self.content = content
		
	def __repr__(self):
		return f'{self.full_name}'
		
	@property
	def full_name(self):
		return self.name + '.' + self.extension
		
	@property
	def vir_fn_prop(self):
		return self.vir_fn()		
		
	def remove_child(self, child: "ObjectTreeNode") -> None:
		pass	

	def add_child(self, child: "ObjectTreeNode") -> None:
		pass
		
	def traverse(self) -> Generator:
		yield self
		
	def as_dict(self, attr):
		
		a = getattr(self,attr)
		
		return a, self.content
		
	def vir_fn(self):
		return PurePosixPath('/'.join([x.full_name for x in reversed(list(self.path_to_top()))][1:]))
		
	def get(self, pathparts):
				
		part = pathparts.pop(0)
		
		if len(pathparts)==0 and part==self.full_name:
			return self
	
				
class VirtualFSFolder(ObjectTreeNode):

	def __init__(self, name = ''):
		
		super().__init__()
		
		self.name = name
			
	def __repr__(self):
		return f'{self.name}/'
		
	@property
	def full_name(self):
		return self.name
		
	@property
	def vir_fn_prop(self):
		return self.vir_fn()		
		
	def vir_fn(self):
		return PurePosixPath('/'.join([x.full_name for x in reversed(list(self.path_to_top()))][1:]))
		
	def get(self, pathparts):
		
		part = pathparts[0]
		
		if not self.is_root:
			pathparts.pop(0)
			
		print(part, pathparts, self.full_name)
		if len(pathparts)==0 and part==self.full_name:
			return self
			
		for ch in self.yield_children(immediate = True):
			if ch.full_name == pathparts[0]:
				return ch.get(pathparts)
	
	def mkdir(self, pathparts):
		
		name = pathparts.pop(0)
		
		exists = False
		for ch in self.yield_children(immediate = True):
			if ch.name == name:
				fld = ch
				exists = True
		
		if not exists:
			fld = VirtualFSFolder(name = name)
			self.add_child(fld)
			
		if len(pathparts)>0:
			fld.mkdir(pathparts)
		
	def touch(self, name, content):
		
		fl = VirtualFSFile(name = name, content = content)
		self.add_child(fl)
		
class VirtualFSRoot(VirtualFSFolder, ObjectTreeRoot):

	def __init__(self, name = ''):
		
		super().__init__(name=name)
		
		
class VirtualFS(ObjectTree):
	
	def __init__(self, root_name = ''):
		
		super().__init__()
		self.root = VirtualFSRoot(name = root_name)
		
	def get(self, path):
		
		if type(path) == str:
			path = PurePosixPath(path)
			
		return self.root.get(list(path.parts))	
		
	def mkdir(self, path):
		
		if type(path) == str:
			path = PurePosixPath(path)
		self.root.mkdir(list(path.parts))
	
	def write_to_disc(self, write_path):
		
		for fsobj in self.traverse():
			if isinstance(fsobj, VirtualFSFile):
				final_path = Path(write_path, fsobj.vir_fn())
				
				Path(final_path.parents[0]).mkdir(parents=True, exist_ok=True)
				
				if isinstance(fsobj.content, str):
					with open(final_path, 'w') as f:
						f.write(fsobj.content)
				elif isinstance(fsobj.content, bytes):
					with open(final_path, 'wb') as f:
						f.write(fsobj.content)
			
	def touch(self, path, content):
		
		if type(path) == str:
			path = PurePosixPath(path)
		
		pathparts = path.parts
		name = pathparts[-1]
		folder_path = None
		if len(pathparts)>1:
			folder_path = Path(*pathparts[:-1])
				
		if folder_path:
			self.root.mkdir(list(folder_path.parts))
			self.get(folder_path).touch(name, content)
		else:
			self.root.touch(name, content)