import re;a=b=0;n="one two three four five six seven eight nine".split()
for l in open("input.txt").readlines():r=re.findall(r"\d",l);a+=int(r[0]+r[-1]);r=re.findall(f"(?=(\\d|{'|'.join(n)}))",l);x,y=r[0],r[-1];b+=int(f"{x if x.isdigit()else n.index(x)+1}{y if y.isdigit()else n.index(y)+1}")
print(a,b)