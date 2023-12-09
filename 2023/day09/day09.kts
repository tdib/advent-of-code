import java.io.File
import kotlin.reflect.typeOf

val lines = File("input.txt").readLines()

fun generateDiffs(line: String): List<MutableList<Int>> {
    val nums = Regex("(-?\\d+)").findAll(line).map { it.value.toInt() }.toMutableList()
    val diffs = mutableListOf(nums)
    while (!diffs.last().all { it == 0 }) {
        val temp = mutableListOf<Int>()
        val curr = diffs.last().toList()
        for (i in 1..<curr.size) {
            temp.add(curr[i] - curr[i-1])
        }
        diffs.add(temp)
    }
    return diffs
}

fun solvePart1(): Int {
    var ans = 0
    for (line in lines) {
        val diffs = generateDiffs(line)
        diffs.last().add(0)

        for (i in (diffs.size-2).downTo(0)) {
            val prev = diffs[i+1].last()
            val curr = diffs[i].last()
            diffs[i].add(curr + prev)
        }
        ans += diffs[0].last()
    }

    return ans
}

fun solvePart2(): Int {
    var ans = 0
    for (line in lines) {
        val diffs = generateDiffs(line)
        diffs.last().add(0, 0)

        for (i in (diffs.size-2).downTo(0)) {
            val prev = diffs[i+1].first()
            val curr = diffs[i].first()
            diffs[i].add(0, curr - prev)
        }
        ans += diffs[0].first()
    }

    return ans
}

println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")
