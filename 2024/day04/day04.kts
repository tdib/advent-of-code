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

fun rotate45(list: List<String>, times: Int): List<String> {
    var retVal: List<String> = list
    for (rotation in 1..times.floorDiv(2)) {
        retVal = rotate90(retVal)
    }
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
    val r = Regex("MAS")
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
            if (subArray[1][1] == 'A') {
                val topLeft = subArray.first().first()
                val topRight = subArray.first().last()
                val bottomLeft = subArray.last().first()
                val bottomRight = subArray.last().last()
                val sanitisedList = listOf(
                    "$topLeft.$topRight",
                    ".A.",
                    "$bottomLeft.$bottomRight"
                )
                var m: List<String>
                var tempTotal = 0
                for (i in 0..7) {
                    m = rotate45(sanitisedList, i)
                    for (l in m) {
                        val matchCount = r.findAll(l).count()
                        tempTotal += matchCount
                    }
                }
                if (tempTotal == 2) {
                    total++
                }
            }
        }
    }

    return total
}

println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")