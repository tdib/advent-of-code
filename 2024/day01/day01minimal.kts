import java.io.File
import kotlin.math.abs

val l = File("test.txt").readLines()
val (a, b) = l
    .map { it.split(Regex("\\s+")).map { it.toInt() } }
    .let { it.map { it[0] }.sorted() to it.map { it[1] }.sorted() }

fun solvePart1() =
    a.zip(b).sumOf { (x, y) -> abs(x - y) }

fun solvePart2() =
    a.fold(0) { x, k -> x + k * (b.groupingBy { it }.eachCount()[k] ?: 0) }

println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")