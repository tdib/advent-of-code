import java.io.File
import kotlin.math.abs

val l = File("input.txt").readLines()

fun f(n: List<Int>) =
    (n.zipWithNext().all { (a, b) -> a < b } || n.zipWithNext().all { (a, b) -> a > b }) &&
    !n.zipWithNext().any { (a, b) -> abs(a - b) > 3 }

fun g(s: String) =
    s.split(" ").map { it.toInt() }

fun solvePart1() =
    l.count { f(g(it)) }

fun solvePart2() =
    l.count {
        val n = g(it)
        (listOf(n) + List(n.size) { n.filterIndexed { i, _ -> i != it } }).any { f(it) }
    }

println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")