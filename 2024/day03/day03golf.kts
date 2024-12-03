val l=java.io.File("input.txt").readLines()
val r="""mul\((\d+),(\d+)\)|do\(\)|don't\(\)"""
var m=0
print("Part 1 answer: ${l.sumOf{Regex(r.take(18)).findAll(it).map{it.groupValues.drop(1).map{it.toInt()}}.map{it[0]*it[1]}.sum()}}\n Part 2 answer: ${l.sumOf{Regex(r).findAll(it).map{it.groupValues}.map{g->var r=0
if(g[0].contains("o("))m=1 else if(g[0].contains("n"))m=0 else r=g[1].toInt()*g[2].toInt()*m
r}.sum()}}")