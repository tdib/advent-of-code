import java.io.File

val lines = File("input.txt").readLines()

// Thank you, Stefan :)
fun solve(values: List<Long>, desiredResult: Long, part: Int, currValue: Long = 0L): Boolean {
    if (currValue == desiredResult && values.isEmpty()) {
        return true
    } else if (currValue > desiredResult || values.isEmpty()) {
        return false
    }
    val valuesMutable = values.toMutableList()
    val nextNum = valuesMutable.removeFirst()

    val resultPlus = currValue + nextNum
    val resultMult = currValue * nextNum
    val resultOr = if (part == 2) (currValue.toString() + nextNum).toLong() else null
    return listOfNotNull(resultPlus, resultMult, resultOr).any { currResult ->
        solve(valuesMutable, desiredResult, part, currResult)
    }
}

fun solvePart(part: Int) =
    lines.sumOf { line ->
        val split = line.split(": ")
        val desiredResult = split.first().toLong()
        val nums = split.last().split(" ").map { it.toLong() }
        if (solve(nums, desiredResult, part = part)) desiredResult else 0
    }

fun solvePart1() = solvePart(1)

fun solvePart2() = solvePart(2)

println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")
