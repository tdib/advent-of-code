import java.io.File

val (dependenciesStr, updatesStr) = File("input.txt").readText().split("\n\n")

val dependencies = dependenciesStr
    .lineSequence()
    .map { line -> line.split("|").map { it.toInt() } }
    .groupBy({ it[0] }, { it[1] })
    .mapValues { (_, values) -> values.toSet() }

val updateVersions = updatesStr
    .lineSequence()
    .map { line -> line.split(",").map { it.toInt() } }

fun isValidUpdate(updates: List<Int>, dependencies: Map<Int, Set<Int>>): Boolean {
    val updatesSoFar = mutableListOf<Int>()
    return updates.all { update ->
        if (updatesSoFar.intersect(dependencies[update].orEmpty()).isEmpty()) {
            updatesSoFar.add(update)
        } else {
            false
        }
    }
}

fun solvePart1() =
    updateVersions.sumOf { updateVersion ->
        if (isValidUpdate(updateVersion, dependencies)) {
            updateVersion[updateVersion.size.floorDiv(2)]
        } else {
            0
        }
    }

fun solvePart2() =
    updateVersions.sumOf { updateVersion ->
        if (!isValidUpdate(updateVersion, dependencies)) {
            val sorted = updateVersion.sortedWith { a, b ->
                when {
                    b in dependencies[a].orEmpty() -> -1 // a depends on b, a < b
                    a in dependencies[b].orEmpty() -> 1 // b depends on a, a > b
                    else -> 0 // no dependency, equal
                }
            }
            sorted[sorted.size.floorDiv(2)]
        } else {
            0
        }
    }

println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")
