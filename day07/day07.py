class Node():
  """
  Node class which represents a file on a file system. It implements a bidirectional
  tree like structure to allow for easy traversal up and down the tree, which is particularly
  useful in commands like `cd ..` or `cd x-directory`.

  @param str name: The name of the file or directory
  @param Node parent: The parent directory (default=None)
  @param int size: The size of the file; directories should have a size of 0 (default=0)
  """
  def __init__(self, name, parent=None, size=0):
    self.name = name
    self.parent = parent
    self.size = size

    self.is_dir = self.size == 0
    self.children = []

  # DFS search to compute size of a node (file/dir)
  def get_size(self):
    total = int(self.size)
    for child in self.children:
      total += child.get_size()
    return total

  # Display files in tree like structure (like example on AOC)
  def display_tree(self, depth=0):
    # Display file information in format:
    # - filename (filetype, size=xxxxxx)
    print(f'{"  " *  depth}- {self.name} ({"dir" if self.is_dir else "file"}, size={self.get_size()})')

    # Recursively call children to display their own subtrees
    for child in self.children:
      child.display_tree(depth+1)

    return ''

  # Consider two nodes equivalent if they have the same name, parent, and file type
  # This allows multiple files with the same name to be in different directories,
  # and files with the same name as its parent directory
  def __eq__(self, other):
      return self.name == other.name\
          and self.parent == other.parent\
          and self.is_dir == other.is_dir

with open('input.txt', 'r') as f:
  lines = f.readlines()

# Keep track of all files/directories (i.e. nodes) within the system
nodes = []
# Keep track of our current directory
working_dir = None

for line in lines:
  split = line.strip().split(' ')

  # Command
  if split[0] == '$':
    # Changing directories
    if split[1] == 'cd':
      target_dir = split[2]

      # Create a temporary node used for comparisons
      temp_node = Node(name=target_dir, parent=working_dir)

      # Go up a directory - use current node's parent
      if target_dir == '..':
        working_dir = working_dir.parent

      # Go to an existing directory in our knowledge base
      elif hasattr(working_dir, 'children') and temp_node in working_dir.children:
        working_dir = [x for x in working_dir.children if x == temp_node][0]

      # We are cding into a new directory - add it to our knowledge base
      else:
        working_dir = Node(name=target_dir, parent=working_dir)
        nodes.append(working_dir)

  # A file has been encountered (i.e. it is the output of an ls command)
  else:
    file_size, file_name = line.strip().split(' ')
    temp_node = Node(name=file_name, parent=working_dir) if file_size == 'dir' else Node(size=file_size, name=file_name, parent=working_dir)
    if temp_node not in nodes:
      nodes.append(temp_node)
    if temp_node not in working_dir.children:
      working_dir.children.append(temp_node)

# Find the sum of all directory nodes with size <= 100000
total_part1 = 0
for node in nodes:
  size = node.get_size()
  if node.is_dir and size <= 100_000:
    total_part1 += size

### Part 2 ###
# Space allocations (given in the question)
TOTAL_DISK = 70_000_000
REQUIRED_UNUSED_SPACE = 30_000_000
# Total size of our system - assumes that the first node is root (/)
used_disk = nodes[0].get_size()
# Compute how much space we need to free up
required_deletion_size = used_disk - (TOTAL_DISK-REQUIRED_UNUSED_SPACE)
# Compute the smallest file that meets the given requirements
smallest_deletable_size = min([node.get_size() for node in nodes if node.is_dir and node.get_size() >= required_deletion_size])
##############

# The following will display the full file system structure - assuming the first node is the root (/)
# nodes[0].display_tree()

print('Part 1 answer:', total_part1, 1581595)
print('Part 2 answer:', smallest_deletable_size, 1544176)