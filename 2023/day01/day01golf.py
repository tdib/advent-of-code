import re;a=b=0;n="_ one two three four five six seven eight nine".split();F=lambda y:int(y) if y.isdigit()else n.index(y);G=re.findall
for l in open("input.txt").readlines():r=G(r"\d",l);a+=int(r[0]+r[-1]);r=G(f"(?=(\\d|{'|'.join(n)}))",l);x,y=r[0],r[-1];b+=10*F(x)+F(y)
print(a,b)