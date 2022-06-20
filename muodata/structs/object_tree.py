# muodata is distributed in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for 
# more details.
# 
# You should have received a copy of the GNU General Public License along 
# with muodata. If not, see <https://www.gnu.org/licenses/>. 

###############################################################################

from typing import Optional, Set, Generator

###############################################################################

class ObjectTreeNode(object):
	

	def __init__(self) -> "ObjectTreeNode":

		self.is_root = False
		
		self.parent = None
		self.children = set()

	def remove(self):

		if self.parent:
			self.parent.remove_child(self)


	def remove_child(self, child: "ObjectTreeNode") -> None:
		
		if child in self.children:
			self.children.remove(child)
	
		child.parent = None
			

	def add_child(self, child: "ObjectTreeNode") -> None:
		
		if child.parent:
			child.parent.remove_child(child)

		self.children.add(child)
		child.parent = self

	def is_orphan(self) -> bool:

		return not (self.is_root or self.parent)
	

	def level(self) -> int:
		
		lvl = 0
		testnode = self

		while testnode != None:
			testnode = testnode.parent
			
			lvl += 1
			
		return lvl


	def traverse(self, sort_attr: Optional[str] = None) -> Generator:
		
		yield self
			
		if not sort_attr:

			for child in self.children:
				yield from child.traverse()
				
		else:
			
			srt = [] # list of tuples (attr; child)
			
			for child in self.children:
				
				if hasattr(child, sort_attr):
					srt.append((getattr(child,sort_attr), child))
				
				else:
					srt.append(('',child))
					
			srt.sort(key=lambda y: y[0])
						
			for cpl in srt:
				yield from cpl[1].traverse(sort_attr = sort_attr)
				


	def yield_children(self, immediate: bool = False) -> Generator:

		for child in self.children:

			if immediate:
				yield child

			else:
				yield from child.traverse()
				
	def as_dict(self, attr):
		
		res = dict()
		
		a = getattr(self,attr)
		
		for child in self.yield_children(immediate = True):
			chattr, chdct = child.as_dict(attr)
			res[chattr] = chdct
			
		return a, res


	def path_to_top(self) -> Generator:

		yield self

		if self.parent:
			yield from self.parent.path_to_top()


	def is_child(self, other: "ObjectTreeNode") -> bool:

		for nd in self.path_to_top():

			if (nd == other) and (nd != self):
				return True

		return False

	
class ObjectTreeRoot(ObjectTreeNode):
	

	def __init__(self) -> "ObjectTreeRoot":
		
		super().__init__()
		self.is_root = True
		
		
class ObjectTree(object):
	

	def __init__(self):
		
		self.root = ObjectTreeRoot()


	def traverse(self, sort_attr: Optional[str] = None):

		yield from self.root.traverse(sort_attr = sort_attr)

	def as_dict(self, attr):
		
		dct = dict()
		for ch in self.root.yield_children(immediate = True):
			chattr, chdct = ch.as_dict(attr)
			dct[chattr] = chdct
		return dct
		