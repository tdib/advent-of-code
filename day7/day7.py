class Node():
  def __init__(self, name, parent=None, size=0):
    self.name = name
    self.parent = parent
    self.size = size
    self.is_dir = self.size == 0
    self.children = []
  
  def get_info(self):
    return f'{self.name} ({"dir" if self.is_dir else self.size}) - parent: {self.parent.name if self.parent else "ROOT"}'

  def get_size(self):
    total = int(self.size)
    for child in self.children:
      total += child.get_size()
    return total

  def display_tree(self, dir_only=False, depth=0):
    size = self.get_size()
    if self.is_dir:
      print(f'{"  " *  depth}- {self.name} (dir, size={size})')
      for child in self.children:
        child.display_tree(dir_only, depth+1)
    elif not self.is_dir and not dir_only:
      print(f'{"  " * depth}- {self.name} (file, size={size})')
    return ''
  
  def __eq__(self, other):
      return self.name == other.name\
          and self.size == other.size\
          and self.parent == other.parent\
          and self.is_dir == other.is_dir

with open('input.txt', 'r') as f:
  lines = f.readlines()

nodes = []
curr_node = None

for line in lines:
  split = line.strip().split(' ')
  # Command
  if split[0] == '$':
    if split[1] == 'cd':
      dir = split[2]
      temp_node = Node(name=dir, parent=curr_node)
      # Go up a directory - use current node's parent
      if dir == '..':
        curr_node = curr_node.parent
      # Go to an existing directory in our knowledge base
      elif hasattr(curr_node, 'children') and temp_node in curr_node.children:
        curr_node = [x for x in curr_node.children if x == temp_node][0]
      # We are cding into a new directory - add it to our knowledge base
      else:
        curr_node = Node(name=dir, parent=curr_node)
        nodes.append(curr_node)
        # print(f'cd to {dir} (NEW)')
      
  # A file has been encountered (i.e. it is the output of an ls command)
  else:
    # print(f'ls command reached - currently in {curr_node.name}')
    file_size, file_name = line.strip().split(' ')
    temp_node = Node(name=file_name, parent=curr_node) if file_size == 'dir' else Node(size=file_size, name=file_name, parent=curr_node)
    if temp_node not in nodes:
      # print(f'new node found: {temp_node.name}')
      nodes.append(temp_node)
    if temp_node not in curr_node.children:
      # print(f'new child found: {temp_node.name}')
      curr_node.children.append(temp_node)
      # print(f'{curr_node.name} is parent of {split[1]}')
    # print('nodes:', nodes)
    # print(f'children of {curr_node.name}: {curr_node.children}')
    # print()

# for node in nodes:
#   print(node.get_info())

# for node in nodes:
#   print(node)

# print([node.name for node in nodes])
# print(nodes[0].display_tree())
# print([node for node in nodes])

total_part1 = 0
for node in nodes:
  size = node.get_size()
  if node.is_dir and size <= 100000:
    total_part1 += size

### Part 2 ###
total_disk = 70_000_000
required_unused_space = 30_000_000
used_disk = nodes[0].get_size()
smallest_deletable_size = used_disk - (total_disk-required_unused_space)
deletable_files = []
for node in nodes:
  if node.is_dir and node.get_size() >= smallest_deletable_size:
    deletable_files.append(node)

# smallest_deletable_file = deletable_files.sort(key=lambda x: x.get_size())
smallest_deletable_file = sorted(deletable_files, key=lambda x: x.get_size())[0]


print('Part 1 answer:', total_part1, 1581595)
print('Part 2 answer:', smallest_deletable_file.get_size(), 1544176)