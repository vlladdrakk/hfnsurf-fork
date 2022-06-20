# muodata is distributed in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for 
# more details.
# 
# You should have received a copy of the GNU General Public License along 
# with muodata. If not, see <https://www.gnu.org/licenses/>. 

###############################################################################

from typing import Set, Any, List, Optional

###############################################################################

class NodeGraph:
	"""Graph of nodes with links between them. Allows to find the
	shortest path between the given nodes.
	"""


	def __init__(self) -> "NodeGraph":
		"""Nodes are formed into a dictionary of sets.

		Example:
		{
			node1: (node2, node3),
			node2: (node1),
			node3: (node1)
		}
		"""

		self.nodes = dict()


	def copy_as_immutable(self) -> dict:
		
		return {key: val for key, val in self.nodes.items()}
	
	
	def restore_from_immutable(self, im: dict) -> None:
		
		self.nodes.clear()
		for key, val in im.items():
			self.nodes[key] = val


	def add_link(self, node1: Any,
						node2: Any) -> None:
		
		"""Add link between nodes. A link is mutual: node1 receives
		a link to node2, while node2 receive a link to node1.

		As the nodes consist of sets, multiple references do not get
		added.
		"""
		
		for node in (node1, node2):
			if not node in self.nodes: self.nodes[node] = set()

		self.nodes[node1].add(node2)
		self.nodes[node2].add(node1)


	def find_path(self, start_node: Any,
						finish_node: Any) -> Optional[List]:
		
		"""Returns a list of nodes that have to be visited
		to arrive from start to finish in the shortest possible
		way.

		Returns None if no such way exists.
		"""

		# If the start and finish nodes are the same, the node
		# itself is returned.

		if start_node == finish_node:
			return [start_node]

		if start_node not in self.nodes:
			return None

		if finish_node not in self.nodes:
			return None

		# This list of lists consist paths, which get recursively followed
		# until the final node is reached.
		paths = [[start_node]]

		# In this set, the already reached nodes are stored, so that
		# superflous paths aren't generated
		reached = set([start_node])

		# If this boolean stays False throughout an iteration, then
		# no more paths are possible and the final node is
		# unreachable
		changed = True

		while changed:

			new_paths = []
			changed = False

			for path in paths:
				
				for dest_node in self.nodes[path[-1]]:

					if not dest_node in reached:
						
						new_path = path[::]
						new_path.append(dest_node)

						if dest_node == finish_node:
							return new_path

						new_paths.append(new_path)
						changed = True

						reached.add(dest_node)

			paths = new_paths[::]

		return None
