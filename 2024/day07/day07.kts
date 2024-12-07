import java.io.File

val lines = File("input.txt").readLines()

enum class Operation {
    MULTIPLY,
    ADD,
    OR;

    companion object {
        fun forPart1() = listOf(MULTIPLY, ADD)
        fun forPart2() = listOf(MULTIPLY, ADD, OR)
    }
}

fun generatePermutations(n: Int, values: List<Operation>): List<List<Operation>> {
    if (n == 1) return listOf(emptyList())
    val smallerPermutations = generatePermutations(n - 1, values)
    return smallerPermutations.flatMap { perm -> values.map { value -> perm + value } }
}

fun solve(part: Int): Long {
    var total = 0L
    for (line in lines) {
        val split = line.split(": ")
        val result = split.first().toLong()
        val nums = split.last().split(" ").map { it.toLong() }
        val permittedOperations = when (part) {
            1 -> Operation.forPart1()
            2 -> Operation.forPart2()
            else -> error("Invalid part number provided")
        }
        val opPerms = generatePermutations(nums.size, permittedOperations)

        for (opPerm in opPerms) {
            var currSum = nums.first()
            for ((num, op) in nums.drop(1).zip(opPerm)) {
                when (op) {
                    Operation.MULTIPLY -> currSum *= num
                    Operation.ADD -> currSum += num
                    Operation.OR -> if (part == 1) {
                        error("Invalid part 1 operation")
                    } else {
                        currSum = (currSum.toString() + num).toLong()
                    }
                }
                if (currSum > result) {
                    break
                }
            }
            if (currSum == result) {
                total += result
                break
            }
        }
    }
    return total

}

fun solvePart1() = solve(part = 1)

fun solvePart2() = solve(part = 2)

println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")
