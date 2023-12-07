import java.io.File

val lines = File("input.txt").readLines()

fun solvePart1(): Int {
    var ans = 1
    val times = "\\d+".toRegex().findAll(lines[0]).map { it.value.toInt() }.toList()
    val dists = "\\d+".toRegex().findAll(lines[1]).map { it.value.toInt() }.toList()

    for ((time, distToBeat) in times.zip(dists)) {
        var winningRaces = mutableListOf<Int>()
        var timeLeft = time
        var distPerMs = 0
        while (timeLeft > 0) {
            timeLeft--
            distPerMs++
            var endDist = timeLeft * distPerMs
            if (endDist > distToBeat) {
                winningRaces.add(endDist)
            }
        }
        ans *= winningRaces.count()
    }

    return ans
}


fun solvePart2(): Int {
    var ans = 0
    val time = "\\d+".toRegex().findAll(lines[0]).joinToString("") { it.value }.toBigInteger()
    val distToBeat = "\\d+".toRegex().findAll(lines[1]).joinToString("") { it.value }.toBigInteger()

    var timeLeft = time
    var distPerMs = 0.toBigInteger()
    while (timeLeft > 0.toBigInteger()) {
        timeLeft--
        distPerMs++
        val endDist = timeLeft * distPerMs
        if (endDist > distToBeat) {
            ans++
        }
    }
    return ans
}


println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")