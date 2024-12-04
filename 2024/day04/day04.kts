import java.io.File

val lines = File("input.txt").readLines()

fun transpose(list: List<String>): List<String> {
    val maxLength = list.maxOfOrNull { it.length } ?: 0
    return (0..<maxLength).map { col ->
        list.mapNotNull { it.getOrNull(col) }.joinToString("")
    }
}

fun rotate90(list: List<String>) =
    list.indices.map { i ->
        list.map { it[i] }.joinToString("").reversed()
    }

/**
 * Rotate an entire matrix 45 degrees, n times
 */
fun rotate45(list: List<String>, times: Int): List<String> {
    var retVal: List<String> = list
    // How many quarter turns
    for (rotation in 1..times.floorDiv(2)) {
        retVal = rotate90(retVal)
    }
    // Add dots to emulate a 45 degree turn, but only we require it (`times` must be divisible by 2)
    if (times % 2 != 0) {
        retVal = retVal.mapIndexed { i, row ->
            List(row.length - i - 1) { "." }.joinToString("") +
                row +
                List(i) { "." }.joinToString("")
        }
        retVal = transpose(retVal)
    }

    return retVal
}

fun solvePart1(): Int {
    val r = Regex("XMAS")
    var m: List<String>
    var total = 0

    for (i in 0..7) {
        m = rotate45(lines, i)
        for (l in m) {
            val matchCount = r.findAll(l).count()
            total += matchCount
        }
    }
    return total
}

fun solvePart2(): Int {
    var total = 0
    val windowHeight = 3
    val windowWidth = 3
    val numRows = lines.size
    val numCols = lines[0].length

    for (row in 0..(numRows - windowHeight)) {
        for (col in 0..(numCols - windowWidth)) {
            val subArray = lines.subList(row, row + windowHeight).map { str ->
                str.substring(col, col + windowWidth)
            }
            val topLeft = subArray.first().first()
            val topRight = subArray.first().last()
            val bottomLeft = subArray.last().first()
            val bottomRight = subArray.last().last()
            val chars = listOf(topLeft, topRight, bottomRight, bottomLeft).joinToString("")
            // We only care about the corner characters, and they must form one of the following, or it is not an X-MAS
            val validCorners = listOf("MMSS", "MSSM", "SSMM", "SMMS")
            if (subArray[1][1] == 'A' && chars in validCorners) {
                total++
            }
        }
    }

    return total
}

println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")