import java.io.File

val l = File("input.txt").readLines()

enum class I(val r: String) {
    M("mul\\((\\d+),(\\d+)\\)"),
    Y("do\\(\\)"),
    D("don't\\(\\)"),
}

fun solvePart1() =
    l.sumOf {
        Regex(I.M.r).findAll(it)
            .map { it.groupValues.drop(1).map { it.toInt() } }
            .map { it[0] * it[1] }
            .sum()
    }

fun solvePart2(): Int {
    var m = 0
    return l.sumOf {
        Regex(I.entries.joinToString("|") { it.r }).findAll(it)
            .map { it.groupValues }
            .map { g ->
                var r = 0
                when (I.entries.find { g[0].matches(it.r.toRegex()) }) {
                    I.Y -> m = 1
                    I.D -> m = 0
                    I.M -> r = g[1].toInt() * g[2].toInt() * m
                    else -> {}
                }
                r
            }
            .sum()
    }
}

println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")