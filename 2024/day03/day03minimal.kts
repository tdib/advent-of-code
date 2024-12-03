import java.io.File

val l = File("input.txt").readLines()

val r = """mul\((\d+),(\d+)\)|do\(\)|don't\(\)"""

fun solvePart1() =
    l.sumOf {
        Regex(r.take(18)).findAll(it)
            .map { it.groupValues.drop(1).map { it.toInt() } }
            .map { it[0] * it[1] }
            .sum()
    }

var m = 0
fun solvePart2() =
    l.sumOf {
        Regex(r).findAll(it)
            .map { it.groupValues }
            .map { g ->
                var r=0
                if (g[0].contains("o(")) m = 1
                else if (g[0].contains("n")) m = 0
                else r = g[1].toInt() * g[2].toInt() * m
                r
            }
            .sum()
    }

println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")