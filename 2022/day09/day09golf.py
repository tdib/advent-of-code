# https://adventofcode.com/2022/day/9

with open('input.txt', 'r') as f:l=map(lambda i:(i[0],int(i[1])),map(str.split,map(str.strip,f.readlines())));R=10;r=[(0,0)]*R;v=set((0,0));m={'R':(1,0),'U':(0,1),'L':(-1,0),'D':(0,-1)}
for d,a in l:
  for _ in[0]*a:
    r[0]=tuple(sum(e)for e in zip(r[0],(max(min(1,m[d][j]),-1)for j in[0,1])))
    for i in range(1,R):
      if any(1<abs(x:=r[i-1][j]-r[i][j])for j in[0,1]):r[i]=tuple(sum(e)for e in zip(r[i],(max(min(1,r[i-1][j]-r[i][j]),-1)for j in[0,1])));v.add(r[i])if i==R-1 else None

# print(f'Answer for part 1 is: {len(v)}') # Variable `R` must be set to 2
print(f'Answer for part 2 is: {len(v)}') # Variable `R` must be set to 10