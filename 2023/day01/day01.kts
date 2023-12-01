import java.io.File

val lines = File("input.txt").readLines()

fun solvePart1(): Int {
    val pattern = Regex("\\d")
    var total = 0
    for (line in lines) {
        // Find all digits
        val matches = pattern.findAll(line)
        if (!matches.any()) { continue }

        // Find the first and last digits out of all of them
        val first = matches.first().value
        val last = matches.last().value

        // Add them to total by concatenating - Since they are strings, we can use + to concatenate
        // (i.e. don't need string interpolation)
        total += (first+last).toInt()
    }
    return total
}

fun solvePart2(): Int {
    val nums = "one two three four five six seven eight nine".split(" ")
    val pattern = Regex("(?=(\\d|${nums.joinToString("|")}))")
    var total = 0
    for (line in lines) {
        // Find all matches and map their values if they are not null (i.e. discard null items)
        val matches = pattern.findAll(line).mapNotNull { it.groups[1]?.value }
        if (!matches.any()) { continue }

        // Get the first match and either convert to int (if it is a digit), or get the value of the digit's word
        var firstStr = matches.first()
        val firstInt = if (firstStr[0].isDigit()) { firstStr.toInt() } else { nums.indexOf(firstStr) + 1 }

        // Do the same as above for the last match
        var lastStr = matches.last()
        val lastInt = if (lastStr[0].isDigit()) { lastStr.toInt() } else { nums.indexOf(lastStr) + 1 }

        // Add to the total - the first int should be in the tens column, hence we multiply by 10, essentially concatenating
        total += 10 * firstInt + lastInt
        // Alternatively, we could concatenate the ints together and then convert them back to an int
        // total += ("$firstInt$lastInt").toInt()
    }
    return total
}

println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")