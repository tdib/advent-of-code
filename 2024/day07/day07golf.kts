val l = java.io.File("input.txt").readLines()
fun s(n:List<Long>,r:Long,p:Int,v:Long):Boolean{if(v==r&&n.isEmpty())return true else if(v>r||n.isEmpty())return false
val m=n[0]
return listOfNotNull(v+m,v*m,if(p>1)(v.toString()+m).toLong()else null).any{s(n.drop(1),r,p,it)}}
fun p(p:Int)=l.sumOf{it.split(": ").let{(a,b)->val r=a.toLong()
if(s(b.split(" ").map{it.toLong()},r,p,0))r else 0}}
print("Part 1 answer: ${p(1)}\nPart 2 answer: ${p(2)}")
