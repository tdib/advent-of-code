c={};h="#";f=lambda n:sum([g("?".join([l.split()[0]]*n),tuple(map(int,l.split()[1].split(",")))*n)for l in open("input.txt").readlines()])
def x(s,n,l):
 if len(s)<1:return int((len(n)==1and l==n[0])or(l==0and len(n)<1))
 if sum(n)<1:return h not in s
 if l==n[0]:return 0if s[0]==h else g(s[1:],n[1:])
 if s[0]==h:return g(s[1:],n,l+1)
 if s[0]==".":return 0if l>0else g(s[1:],n)
 return g(s[1:],n,l+1) if l>0 else g(s[1:],n)+g(s[1:],n,l+1)
def g(s,n,l=0):
 k=(s,n,l)
 if k not in c:
  c[k]=x(s,n,l)
 return c[k]
print(f(1),f(5))