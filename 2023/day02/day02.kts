import java.io.File

val lines = File("./input.txt").readLines()

enum class Colour {
    Red,
    Green,
    Blue;

    companion object {
        fun fromStr(s: String): Colour = when (s) {
            "red" -> Red
            "green" -> Green
            "blue" -> Blue
            else -> throw IllegalArgumentException("Unknown colour: $s")
        }
    }
}

fun getHighestCounts(line: String) = line
    // ["3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"]
    .split(": ")[1]
    // [["3 blue, 4 red"], ["1 red, 2 green, 6 blue"], ["2 green"]]
    .split("; ")
    // ["3 blue", "4 red", "1 red", "2 green", "6 blue", "2 green"]
    .flatMap { group -> group.split(", ")}
    // Find highest of each colour in this game - (4, 2, 6)
    .fold(intArrayOf(0, 0, 0)) { acc, cubes ->
        val (amountStr, colourStr) = cubes.split(" ")
        val amount = amountStr.toInt()
        val colour = Colour.fromStr(colourStr)
        acc[colour.ordinal] = maxOf(acc[colour.ordinal], amount)
        acc
    }

fun solvePart1(): Int {
    // Define the most of any given colour we can have in the format (r, g, b)
    val maxBounds = listOf(12, 13, 14)
    var ans = 0
    for ((i, line) in lines.withIndex()) {
        val gameIndex = i + 1
        val highestCounts = getHighestCounts(line)
        if (highestCounts.zip(maxBounds).all { (count, maxBound) -> count <= maxBound }) {
            ans += gameIndex
        }
    }

    return ans
}

fun solvePart2(): Int {
    var ans = 0
    for (line in lines) {
        val highestCounts = getHighestCounts(line)
        ans += highestCounts.reduce { acc, count -> acc * count }
    }

    return ans
}

println("Part 1 answer ${solvePart1()}")
println("Part 2 answer ${solvePart2()}")
