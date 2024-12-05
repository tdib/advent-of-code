val (i,j)=java.io.File("input.txt").readText().split("\n\n")
val d=i.lineSequence().map{it.split("|").map{it.toInt()}}.groupBy({it[0]},{it[1]})
val u=j.lineSequence().map{line->line.split(",").map{it.toInt()}}
var x=0
var y=0
fun v(n:List<Int>)=n.fold(listOf<Int>()){a,b->if(a.intersect(d[b].orEmpty()).isEmpty())a+b else return false}.let{true}
u.forEach{if(v(it)){x+=it[it.size.floorDiv(2)]}else{y+=it.sortedWith{a,b->when{b in d[a].orEmpty()->-1
a in d[b].orEmpty()->1 else->0}}[it.size.floorDiv(2)]}}
print("Part 1 answer: $x\nPart 2 answer: $y")
