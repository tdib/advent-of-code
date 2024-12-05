import java.io.File

val (ds, us) = File("input.txt").readText().split("\n\n")
val d = ds.lineSequence().map { it.split("|").map { it.toInt() } }.groupBy({ it[0] }, { it[1] })
val u = us.lineSequence().map { line -> line.split(",").map { it.toInt() } }

fun v(n: List<Int>) = n.fold(listOf<Int>()) { a, b -> if (a.intersect(d[b].orEmpty()).isEmpty()) a+b else return false }.let{ true }

var x = 0
var y = 0

u.forEach {
    if (v(it)) {
        x += it[it.size.floorDiv(2)]
    } else {
        y += it.sortedWith { a, b ->
            when {
                b in d[a].orEmpty() -> -1
                a in d[b].orEmpty() -> 1
                else -> 0
            }
        }[it.size.floorDiv(2)]
    }
}

println("Part 1 answer: $x")
println("Part 2 answer: $y")
