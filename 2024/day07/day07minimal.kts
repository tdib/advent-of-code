import java.io.File

val l = File("input.txt").readLines()

// Thank you, Stefan :)
fun solve(l: List<Long>, r: Long, p: Int, v: Long): Boolean {
    if (v == r && l.isEmpty()) return true  else if (v > r || l.isEmpty()) return false
    val n = l.toMutableList()
    val m = n.removeFirst()
    return listOfNotNull(
        v + m,
        v * m,
        if (p > 1) (v.toString() + m).toLong() else null
    ).any { currResult ->
        solve(n, r, p, currResult)
    }
}

fun solvePart(p: Int) =
    l.sumOf {
        it.split(": ").let { (a, b) ->
            val r = a.toLong()
            if (solve(b.split(" ").map { it.toLong() }, r, p, 0)) r else 0
        }
    }

fun solvePart1() = solvePart(1)

fun solvePart2() = solvePart(2)

println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")
