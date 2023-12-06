import java.io.File
import kotlin.math.pow

val lines = File("input.txt").readLines()

fun solvePart1(): Int {
    var ans = 0.0
    for (line in lines.withIndex()) {
        // Get sets of the winning numbers and our picks
        var (winning, mine) = line.value
            .split(":")[1]
            .split("|")
            .map { nums ->
                nums
                    .trim()
                    .split("\\s+".toRegex())
                    .map { num -> num.trim().toInt() }
                    .toSet()
            }

        // The intersection of winning numbers and ours is the number of wins
        val numWins = winning.intersect(mine).size
        if (numWins > 0) {
            // 2^{n-1}
            ans += 2.toDouble().pow(numWins - 1)
        }
    }

    return ans.toInt()
}


fun solvePart2(): Int {
    var copies = hashMapOf<Int, Int>()
    // We know we will have at least one copy of each card
    for (i in 1..lines.size) {
        copies[i] = 1
    }
    for (line in lines.withIndex()) {
        // Get the winning and our picks
        var (winning, mine) = line.value
            .split(":")[1]
            .split("|")
            .map { nums ->
                nums
                    .trim()
                    .split("\\s+".toRegex())
                    .map { num -> num.trim().toInt() }
                    .toSet()
            }

        val numWins = winning.intersect(mine).size
        val gameId = line.index+1

        // Increment next n scratchcard copies
        for (i in gameId + 1..gameId + numWins) {
            copies[i] = copies[i]!! + copies[gameId]!!
        }
    }

    return copies.values.sum()
}


println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")