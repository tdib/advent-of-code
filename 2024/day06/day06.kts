import java.io.File

val lines = File("input.txt").readLines()
val map = lines.map { line -> line.map { it }}
val startPosition = findStartPosition()
val simulationVisited = simulate()

typealias Map = List<List<Char>>

data class Position(val row: Int, val col: Int) {
    fun move(direction: Direction): Position =
        Position(
            this.row + direction.deltaRow,
            this.col + direction.deltaCol
        )

    fun isWall(m: Map = map) = m[row][col] == '#'

    fun isWithinBounds(m: Map = map) = (row >= 0) && (row < m.size) && (col >= 0) && (col < m[0].size)
}

data class PositionDirection(val position: Position, val direction: Direction) {
    fun move(direction: Direction) = PositionDirection(this.position.move(direction), direction)
}

enum class Direction(val deltaRow: Int, val deltaCol: Int) {
    UP(-1, 0),
    RIGHT(0, 1),
    DOWN(1, 0),
    LEFT(0, -1),
}

fun <T> List<T>.cycle(): MutableList<T> = (drop(1) + take(1)).toMutableList()

fun findStartPosition(): Position {
    for ((rowIdx, row) in map.withIndex()) {
        for ((colIdx, col) in row.withIndex()) {
            if (col == '^') {
                return Position(rowIdx, colIdx)
            }
        }
    }
    throw Exception("Could not find start position")
}

/**
 * Find the set of visited positions in the map
 */
fun simulate(): Set<Position> {
    var directions = Direction.entries.toMutableList()
    var currPos = startPosition
    val visited = mutableSetOf(currPos)
    var currDirection = directions.first()

    while (currPos.isWithinBounds()) {
        val targetPos = currPos.move(currDirection)
        when {
            !targetPos.isWithinBounds() -> {
                break
            }

            !targetPos.isWall() -> {
                // We can freely move in this direction
                currPos = targetPos
            }

            targetPos.isWall() -> {
                // We have to turn 90 degrees
                directions = directions.cycle()
                currDirection = directions.first()
            }
        }
        visited.add(currPos)
    }

    return visited
}

/**
 * Run a simulation on an adjusted map, tracking visited states (that include both position and direction).
 *
 * If a cycle is detected, return true, otherwise false.
 */
fun hasCycle(map: List<List<Char>>): Boolean {
    var directions = Direction.entries.toMutableList()
    val visited = mutableSetOf<PositionDirection>()

    var currDirection = directions.first()
    var currPositionDirection = PositionDirection(startPosition, currDirection)

    visited.add(currPositionDirection)
    while (currPositionDirection.position.isWithinBounds(map)) {
        val targetPos = currPositionDirection.move(currDirection)
        when {
            !targetPos.position.isWithinBounds(map) -> {
                break
            }

            !targetPos.position.isWall(map) -> {
                // We can freely move in this direction
                if (targetPos in visited) {
                    return true
                } else {
                    currPositionDirection = targetPos
                }
            }

            else -> {
                // We have to turn 90 degrees
                directions = directions.cycle()
                currDirection = directions.first()
            }
        }
        visited.add(currPositionDirection)
    }

    return false
}

fun solvePart1() = simulationVisited.size

fun solvePart2(): Int {
    var total = 0
    for ((rowIdx, row) in map.withIndex()) {
        for ((colIdx, _) in row.withIndex()) {
            // The initial simulation never visits this spot, so this obstacle would have no effect
            if (!simulationVisited.contains(Position(rowIdx, colIdx))) {
                continue
            }
            // Create a temporary map with a new obstacle and detect any cycles
            val tempMap = map.map { it.toMutableList() }.apply { this[rowIdx][colIdx] = '#' }
            if (hasCycle(tempMap)) {
                total++
            }
        }
    }
    return total
}

println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")
