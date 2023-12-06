S=[];m=s=0
for l in open("input.txt").readlines():
 if l=="\n":S+=[s];s=0
 else:s+=int(l)
S.sort();print(f"{' '.join([str(sum(S[-n:]))for n in[1,3]])}")