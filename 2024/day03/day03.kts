import java.io.File

val lines = File("input.txt").readLines()

enum class Instruction(val regexStr: String) {
    MUL("mul\\((\\d+),(\\d+)\\)"),
    DO("do\\(\\)"),
    DONT("don't\\(\\)"),
}

fun String.toInstruction() = Instruction.entries.find { this.matches(it.regexStr.toRegex()) }

fun solvePart1(): Int {
    return lines.sumOf {
        Regex(Instruction.MUL.regexStr).findAll(it)
            .map { matchResult -> matchResult.groupValues }
            .map { groupValues -> groupValues[1].toInt() * groupValues[2].toInt() }
            .sum()
    }
}

fun solvePart2(): Int {
    var shouldMultiply = true
    return lines.sumOf { line ->
        Regex(Instruction.entries.joinToString("|") { it.regexStr }).findAll(line)
            .map { matchResult -> matchResult.groupValues }
            .map { groupValues ->
                when (groupValues[0].toInstruction()) {
                    Instruction.DO ->  shouldMultiply = true
                    Instruction.DONT -> shouldMultiply = false
                    Instruction.MUL -> if (shouldMultiply) {
                        return@map groupValues[1].toInt() * groupValues[2].toInt()
                    }
                    else -> Unit
                }
                0
            }
            .sum()
    }
}

println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")