fun f(n:List<Int>)=(n.zipWithNext().all{(a,b)->a<b}||n.zipWithNext().all{(a,b)->a>b})&&!n.zipWithNext().any{(a,b)->kotlin.math.abs(a-b)>3}
fun g(s:String)=s.split(" ").map{it.toInt()}
val l=java.io.File("input.txt").readLines()
print("Part 1 answer: ${l.count{f(g(it))}}\nPart 2 answer: ${l.count{val n=g(it);(listOf(n)+List(n.size){n.filterIndexed{i,_->i!=it}}).any{f(it)}}}")
