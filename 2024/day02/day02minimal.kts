import java.io.File

fun f(n: List<Int>): Boolean {
    val d = n.zipWithNext().map { (a, b) -> a - b }
    return d.all { it in 1..3 } || d.all { it in -3..-1 }
}

val n = File("input.txt").readLines().map { it.split(" ").map { it.toInt() }}

fun solvePart1() =
    n.count { f(it) }

fun solvePart2() =
    n.count { List(it.size) { j -> it.filterIndexed { i, _ -> i != j } }.any { f(it) } }

println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")