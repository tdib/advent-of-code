import java.io.File
import java.util.*

val diskMap = File("input.txt").readLines().first()

sealed interface DiskStatus {
    data class Filled(val value: Int) : DiskStatus
    data object Empty : DiskStatus
}

typealias Disk = List<DiskStatus>
typealias Disk2 = List<MemoryBlock>

fun calculateChecksum(disk: Disk): Long =
    disk.withIndex().sumOf { (idx, diskStatus) ->
        ((diskStatus as? DiskStatus.Filled)?.let {
            idx * it.value
        } ?: 0).toLong()
    }

fun solvePart1(): Long {
    val disk = mutableListOf<DiskStatus>()
    diskMap.chunked(2).map { chunk ->
        chunk.map { it.digitToInt() }
    }.forEachIndexed { idx, digits ->
        val (numFilled, numEmpty) = if (digits.size == 2) {
            digits
        } else {
            listOf(digits.first(), 0)
        }
        disk.addAll(
            List(numFilled) { DiskStatus.Filled(idx) } + List(numEmpty) { DiskStatus.Empty }
        )
    }

    var lPtr = 0
    var rPtr = disk.size - 1
    while (lPtr < rPtr) {
        while (disk[lPtr] is DiskStatus.Filled) {
            lPtr++
        }
        while (disk[rPtr] is DiskStatus.Empty) {
            rPtr--
        }

        if (lPtr < rPtr) {
            Collections.swap(disk, lPtr, rPtr)
        }
    }

    return calculateChecksum(disk)
}

sealed interface MemoryBlock {
    val size: Int
    val startIdx: Int
    data class Filled(override val size: Int, override var startIdx: Int, val value: Int) : MemoryBlock
    data class Empty(override var size: Int, override var startIdx: Int, ) : MemoryBlock
}

fun solvePart2(): Long {
    val files = mutableListOf<MemoryBlock.Filled>()
    val spaces = mutableListOf<MemoryBlock.Empty>()
    var startIdx = 0
    diskMap.chunked(2).map { chunk ->
        chunk.map { it.digitToInt() }
    }.forEachIndexed { idx, digits ->
        val numFilled = digits.first()
        files.add(MemoryBlock.Filled(numFilled, startIdx, idx))
        startIdx += numFilled
        val numEmpty = if (digits.size == 2) digits.last() else 0
        if (numEmpty > 0) {
            spaces.add(MemoryBlock.Empty(numEmpty, startIdx))
            startIdx += numEmpty
        }
    }

    val movedFiles = mutableListOf<MemoryBlock.Filled>()
    for (fileIdx in files.lastIndex downTo 0) {
        val file = files[fileIdx]
        val emptySpaceStartIdx = spaces.indexOfFirst { space ->
            space.size >= file.size
        }

        // There is no empty space at all or no empty space to the left of the file
        if (emptySpaceStartIdx == -1 || spaces[emptySpaceStartIdx].startIdx > file.startIdx) {
            // The file does not change
            movedFiles.add(file)
            continue
        }

        val emptySpace = spaces[emptySpaceStartIdx]
        val originalStart = emptySpace.startIdx

        spaces[emptySpaceStartIdx].startIdx += file.size
        spaces[emptySpaceStartIdx].size -= file.size
        files[fileIdx].startIdx = originalStart

        movedFiles.add(MemoryBlock.Filled(file.size, originalStart, file.value))
    }

    var ans = 0L
    for (f in movedFiles) {
        for (i in 0..<f.size) {
            ans += f.value * (f.startIdx + i)
        }
    }
    return ans
}

println("Part 1 answer: ${solvePart1()}")
println("Part 2 answer: ${solvePart2()}")
