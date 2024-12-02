import java.io.File
import kotlin.math.abs

val lines = File("input.txt").readLines()

enum class Direction {
    INCREASING,
    DECREASING,
    NONE,
}

fun getDirection(nums: List<Int>): Direction {
    val isAscending = nums.zipWithNext().all { it.first < it.second }
    val isDescending = nums.zipWithNext().all { it.first > it.second }

    return if (isAscending) {
        Direction.INCREASING
    } else if (isDescending) {
        Direction.DECREASING
    } else {
        Direction.NONE
    }
}

fun isSafe(nums: List<Int>, threshold: Int = 3) =
    nums.zipWithNext().any { (prev, curr) -> abs(prev - curr) > threshold }.not()

fun Boolean.toInt() = if (this) 1 else 0

val r = Regex("\\d+")
fun solvePart1() =
    lines.sumOf { line ->
        val nums = r.findAll(line).map { it.value.toInt() }.toList()
        (getDirection(nums) != Direction.NONE && isSafe(nums)).toInt()
    }

fun solvePart2() =
    lines.sumOf { line ->
        val nums = r.findAll(line).map { it.value.toInt() }.toList()
        val numsRemoved = listOf(nums) + List(nums.size) { index ->
            nums.filterIndexed { i, _ -> i != index }
        }
        numsRemoved.any { trial ->
            getDirection(trial) != Direction.NONE && isSafe(trial)
        }.toInt()
    }

println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")