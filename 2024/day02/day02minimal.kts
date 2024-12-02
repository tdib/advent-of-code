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
    l.count { List(g(it).size) { j -> g(it).filterIndexed { i, _ -> i != j } }.any { f(it) } }

println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")