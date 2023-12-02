a=0;p=[]
for i,l in enumerate(open("input.txt").readlines()):
 c=[0]*3
 for g in l.split(":")[1].split(";"):
  for e in g.split(","):n,x=e.split();x=len(x)-3;c[x]=max(c[x],int(n))
 a+=c[0]*c[1]*c[2];p.append((i+1)*all(c[x]<(13,14,15)[x]for x in(0,1,2)))
print(sum(p),a)