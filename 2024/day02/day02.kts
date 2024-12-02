import java.io.File
import kotlin.math.abs

val lines = File("input.txt").readLines()

enum class Direction {
    INCREASING,
    DECREASING,
    NONE,
}
val threshold = 3

fun getDirection(nums: List<Int>): Direction {
    val ascending = nums.zipWithNext().all { it.first < it.second }
    val descending = nums.zipWithNext().all { it.first > it.second }

    return if (ascending) {
        Direction.INCREASING
    } else if (descending) {
        Direction.DECREASING
    } else {
        Direction.NONE
    }
}

fun isSafe(nums: List<Int>, threshold: Int = 2): Boolean {
    var currNum = nums.first()
    var isSafe = true
    for (num in nums.drop(1)) {
        if (abs(currNum - num) > threshold) {
            isSafe = false
            break
        } else {
            currNum = num
        }
    }
    return isSafe
}

fun solvePart1(): Int {
    val r = Regex("\\d+")
    var total = 0
    val threshold = 3
    for (line in lines) {
        val nums = r.findAll(line).map { it.value.toInt() }.toList()
        when (getDirection(nums)) {
            Direction.INCREASING -> {
                total += if (isSafe(nums, threshold)) 1 else 0
            }

            Direction.DECREASING -> {
                total += if (isSafe(nums, threshold)) 1 else 0
            }

            Direction.NONE -> Unit
        }
    }
    return total
}

fun solvePart2(): Int {
    val r = Regex("\\d+")
    var total = 0
    for (line in lines) {
        val nums = r.findAll(line).map { it.value.toInt() }.toList()
        val numsRemoved = listOf(nums) + List(nums.size) { index ->
            nums.filterIndexed { i, _ -> i != index }
        }
        for (trial in numsRemoved) {
            if (getDirection(trial) != Direction.NONE) {
                if (isSafe(trial, threshold)) {
                    total += 1
                    break
                }
            }
        }
    }
    return total
}

println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")