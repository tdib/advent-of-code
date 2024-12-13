import java.io.File

val map = File("input.txt").readLines()

object KEY {
    const val EMPTY = '.'
}

data class Position(val row: Int, val col: Int) {
    fun isWithinBounds() = row >= 0 && row < map.size && col >= 0 && col < map[0].length
}

/**
 * Given a frequency (character), find the positions of all corresponding frequencies
 */
fun findAllFrequencyPositions(frequency: Char): Set<Position> {
    val frequencyPositions = mutableSetOf<Position>()
    for ((ri, r) in map.withIndex()) {
        for ((ci, c) in r.withIndex()) {
            if (c == frequency) {
                frequencyPositions.add(Position(ri, ci))
            }
        }
    }
    return frequencyPositions
}

fun getAntinodePositions(frequencyPositions: Set<Position>, part: Int): Set<Position> {
    val antinodePositions = mutableSetOf<Position>()
    for (frequencyPosition in frequencyPositions) {
        val otherFrequencyPositions = frequencyPositions.filter { it != frequencyPosition }
        for (otherFrequencyPosition in otherFrequencyPositions) {
            val deltaPosition = calculateDelta(frequencyPosition, otherFrequencyPosition)
            when (part) {
                1 ->  {
                    val potentialAntinodePosition = getNextAntinodePosition(frequencyPosition, deltaPosition)
                    if (potentialAntinodePosition.isWithinBounds()) {
                        antinodePositions.add(potentialAntinodePosition)
                    }
                }

                2 -> {
                    var potentialAntinodePosition = getNextAntinodePosition(otherFrequencyPosition, deltaPosition)
                    while (potentialAntinodePosition.isWithinBounds()) {
                        antinodePositions.add(potentialAntinodePosition)
                        potentialAntinodePosition = getNextAntinodePosition(potentialAntinodePosition, deltaPosition)
                    }
                }

                else -> error("Invalid part provided")
            }

        }
    }
    return antinodePositions
}

fun calculateDelta(currPos: Position, otherPos: Position) =
    Position(currPos.row - otherPos.row, currPos.col - otherPos.col)

fun getNextAntinodePosition(frequencyPosition: Position, deltaPosition: Position): Position {
    val newRow = frequencyPosition.row + deltaPosition.row
    val newCol = frequencyPosition.col + deltaPosition.col
    val potentialAntinodePosition = Position(newRow, newCol)
    return potentialAntinodePosition
}

fun solve(part: Int): Int {
    val visitedFrequencies = mutableSetOf<Char>()
    val antinodePositions = mutableSetOf<Position>()
    for (r in map) {
        for (c in r) {
            if (c == KEY.EMPTY || c in visitedFrequencies) continue

            visitedFrequencies.add(c)
            val frequencyPositions = findAllFrequencyPositions(c)
            antinodePositions.addAll(getAntinodePositions(frequencyPositions, part))
        }
    }
    return antinodePositions.size
}

fun solvePart1() = solve(part = 1)

fun solvePart2() = solve(part = 2)

println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")
