from networkx import*;g=Graph()
for l in open("input.txt").readlines():n,c=l.split(":");[g.add_edge(n,q)for q in c.split()]
g.remove_edges_from(minimum_edge_cut(g))
a,b=map(len,connected_components(g))
print(a*b)