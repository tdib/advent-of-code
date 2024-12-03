import java.io.File

val lines = File("input.txt").readLines()

fun solvePart1(): Int {
    return lines.sumOf {
        Regex("mul\\((\\d+),(\\d+)\\)").findAll(it)
            .map { matchResult -> matchResult.groupValues }
            .map { groupValues -> groupValues[1].toInt() * groupValues[2].toInt() }
            .sum()
    }
}

enum class Instruction {
    MUL,
    DO,
    DONT;
}

fun String.toInstruction() = when {
    this.matches(Regex("mul\\((\\d+),(\\d+)\\)")) -> Instruction.MUL
    this.matches(Regex("do\\(\\)")) -> Instruction.DO
    this.matches(Regex("don't\\(\\)")) -> Instruction.DONT
    else -> null
}

fun solvePart2(): Int {
    var shouldMultiply = true
    return lines.sumOf {
        Regex("mul\\((\\d+),(\\d+)\\)|do\\(\\)|don't\\(\\)").findAll(it)
            .map { matchResult -> matchResult.groupValues }
            .map { groupValues ->
                when (groupValues[0].toInstruction()) {
                    Instruction.DO ->  shouldMultiply = true
                    Instruction.DONT -> shouldMultiply = false
                    Instruction.MUL -> if (shouldMultiply) {
                        return@map groupValues[1].toInt() * groupValues[2].toInt()
                    }
                    else -> throw Exception()
                }
                0
            }
            .sum()
    }
}

println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")