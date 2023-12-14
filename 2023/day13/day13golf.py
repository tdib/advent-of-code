l=[x.split()for x in open("input.txt").read().split("\n\n")];a=0;b=0
def f(g,p=0):
 n=len(g)
 for i in range(1,n):
  t=g[:i][::-1][:n-i];b=g[i:][:i]
  if(p<1and t==b)or(p and sum([m!=n for x,y in zip(t,b) for m,n in zip(x,y)])==1):return i
 return 0
for g in l:
 t=list(zip(*g))
 if r:=f(g):a+=100*r
 else:a+=f(t)
 if r:=f(g,1):b+=100*r
 else:b+=f(t,1)
print(a,b)