fun f(n:List<Int>):Boolean{val d=n.zipWithNext().map{(a,b)->a-b}
return d.all{it in 1..3}||d.all{it in-3..-1}}
val n=java.io.File("input.txt").readLines().map{it.split(" ").map{it.toInt()}}
print("Part 1 answer: ${n.count(::f)}\nPart 2 answer: ${n.count{List(it.size){j->it.filterIndexed{i,_->i!= j}}.any(::f)}}")
