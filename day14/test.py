


l = [(1, 5), (5, 5)]

b = [(x, 5) for x in range(l[0][0]+1, l[1][0])]
print(l)
print(b)

a = []
a.append(l)
a.append(b)
print(a)
