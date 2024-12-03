val l=java.io.File("input.txt").readLines()
enum class I(val r:String){M("mul\\((\\d+),(\\d+)\\)"),Y("do\\(\\)"),D("don't\\(\\)")}var m=0
print("Part 1 answer: ${l.sumOf{Regex(I.M.r).findAll(it).map{it.groupValues.drop(1).map{it.toInt()}}.map{it[1]*it[2]}.sum()}}\nPart 2 answer: ${l.sumOf{Regex(I.entries.joinToString("|"){it.r}).findAll(it).map{it.groupValues}.map{g->when(I.entries.find{g[0].matches(it.r.toRegex())}){I.Y->m=1
I.D->m=0 else->{}}
g[1].toInt()*g[2].toInt()*m}
.sum()}}")