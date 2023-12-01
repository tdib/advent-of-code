import re;a=0;b=0;n=["one","two","three","four","five","six","seven","eight","nine"];p=f"(?=(\\d|{'|'.join(n)}))"
for l in open("input.txt").readlines():r=re.findall(r"\d",l);a+=int(r[0]+r[-1]);r=re.findall(p,l);b+=int(f"{r[0]if r[0].isdigit()else n.index(r[0])+1}{r[-1]if r[-1].isdigit()else n.index(r[-1])+1}")
print(a);print(b)