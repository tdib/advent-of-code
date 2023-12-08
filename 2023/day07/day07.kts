import java.io.File

val lines = File("input.txt").readLines()

fun classifyHand(hand: String, isPart2: Boolean): Int {
    val counts = hand.groupBy { it }.mapValues { (_, values) -> values.size }.toMutableMap()
    var jCount = counts.getOrDefault('J', 0)
    if (isPart2) {
        counts.remove('J')
    } else {
        jCount = 0
    }

    return when {
        // Five of a kind
        counts.containsValue(5 - jCount) || jCount >= 4 -> 7
        // Four of a kind
        counts.containsValue(4 - jCount) -> 6
        // Full house
        (counts.filter { it.value == 2 }.size == 2 && jCount == 1) || (counts.containsValue(3) && counts.containsValue(2)) -> 5
        // Three of a kind
        counts.containsValue(3 - jCount) -> 4
        // Two pair
        counts.filter { it -> it.value == 2 }.size == 2 -> 3
        // One pair
        counts.containsValue(2 - jCount) -> 2
        // High card
        else -> 1
    }
}

fun createHandComparator(labels: List<Char>): Comparator<String> =
    Comparator { s1: String, s2: String ->
        s1.zip(s2).map { (c1, c2) ->
            labels.indexOf(c2) - labels.indexOf(c1)
        }.find { it != 0 } ?: 0
    }

fun sortWins(allWins: List<Triple<Int, String, Int>>, labels: List<Char>): List<Triple<Int, String, Int>> {
    val handComparator = createHandComparator(labels)
    return allWins.sortedWith(
        compareBy {
                a: Triple<Int, String, Int> -> a.first
        }.thenComparing {
                a, b -> handComparator.compare(a.second, b.second)
        }
    )
}

fun solvePart1(): Int {
    val labels = "A K Q J T 9 8 7 6 5 4 3 2".split(" ").map { it[0] }

    val allWins = mutableListOf<Triple<Int, String, Int>>()
    for (line in lines) {
        val (hand, winnings) = line.split(" ")
        allWins.add(Triple(classifyHand(hand, false), hand, winnings.toInt()))
    }

    val sortedWins = sortWins(allWins, labels)
    return sortedWins.mapIndexed { idx, triple -> triple.third * (idx + 1) }.sum()
}

fun solvePart2(): Int {
    val labels = "A K Q T 9 8 7 6 5 4 3 2 J".split(" ").map { it[0] }

    val allWins = mutableListOf<Triple<Int, String, Int>>()
    for (line in lines) {
        val (hand, winnings) = line.split(" ")
        allWins.add(Triple(classifyHand(hand, true), hand, winnings.toInt()))
    }

    val sortedWins = sortWins(allWins, labels)
    return sortedWins.mapIndexed { idx, triple -> triple.third * (idx + 1) }.sum()
}

println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")