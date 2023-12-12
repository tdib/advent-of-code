import java.io.File

val lines = File("input.txt").readLines()

data class NumPos(val value: Int, val row: Int, val colRange: IntRange)
data class SymPos(val value: Char, val rowRange: IntRange, val colRange: IntRange)

fun parseGrid(): Pair<Set<NumPos>, Set<SymPos>> {
    val numRe = "(\\d+)".toRegex()
    val symRe = "[^\\d.]".toRegex()
    val nums = mutableSetOf<NumPos>()
    val syms = mutableSetOf<SymPos>()
    for ((row, line) in lines.withIndex()) {
        numRe.findAll(line).forEach { nums.add(NumPos(it.value.toInt(), row, it.range)) }
        symRe.findAll(line).forEach { syms.add(SymPos(it.value[0], row-1..row+1, it.range.first-1..it.range.last+1)) }
    }

    return Pair(nums, syms)
}

fun p1(): Int {
    val (nums, syms) = parseGrid()

    // Find the numbers that are not touching a symbol
    val notTouching = nums.toMutableSet()
    for (s in syms) {
        for (r in s.rowRange) {
            for (c in s.colRange) {
                nums.filter { it.row == r && c in it.colRange }.forEach { notTouching.remove(it) }
            }
        }
    }
    // The difference between all numbers and the ones that are not touching will give us only the touching ones
    val touching = nums - notTouching

    // Sum the value of all touching numbers
    return touching.sumOf { it.value }
}

fun p2(): Int {
    var total = 0
    val (nums, syms) = parseGrid()

    for (s in syms) {
        // We only care about gears
        if (s.value != '*') { continue }

        // Compute what numbers are touching this gear
        val touching = mutableSetOf<NumPos>()
        for (r in s.rowRange) {
            for (c in s.colRange) {
                touching.addAll(nums.filter { it.row == r && c in it.colRange })
            }
        }

        // If there are 2+ numbers touching this, then add the product to the total
        if (touching.size >= 2) {
            total += touching.map { it.value }.fold(1) { acc, numPos -> acc * numPos }
        }
    }

    return total
}

println("Part 1 answer ${p1()}")
println("Part 2 answer ${p2()}")