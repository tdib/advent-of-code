import java.io.File
import kotlin.math.abs

val lines = File("input.txt").readLines()

fun solvePart1(): Int {
    val r = Regex("\\d+")
    val listA = mutableListOf<Int>()
    val listB = mutableListOf<Int>()

    for (line in lines) {
        r.findAll(line).map { it.value.toInt() }.apply {
            listA.add(this.first())
            listB.add(this.last())
        }
    }

    listA.sort()
    listB.sort()

    return listA.zip(listB).sumOf { abs(it.first - it.second) }
}

fun solvePart2(): Int {
    val r = Regex("\\d+")
    val listA = mutableListOf<Int>()
    val listB = mutableListOf<Int>()

    for (line in lines) {
        val nums = r.findAll(line).map { it.value }.toList()
        listA.add(nums.first().toInt())
        listB.add(nums.last().toInt())
    }

    val counts = listB.groupingBy { it }.eachCount()
    return listA.fold(0) { acc, item ->
        acc + item * counts.getOrDefault(item, 0)
    }
}

println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")