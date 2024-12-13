import java.io.File
import java.util.*

val diskMap = File("input.txt").readLines().first()

sealed interface DiskStatus {
    data class Filled(val value: Int) : DiskStatus
    data object Empty : DiskStatus
}

typealias Disk = List<DiskStatus>
typealias Disk2 = List<MemoryBlock>

fun Disk2.toStringRepr(): String = buildString {
    this@toStringRepr.forEach {
        append(
            when (it) {
                is MemoryBlock.Filled -> (it.value).toString().repeat(it.size)
                else -> '.'.toString().repeat(it.size)
            }
        )
    }
}

fun printDisk(disk: Disk) {
    println(
        disk.map {
            when (it) {
                is DiskStatus.Filled -> it.value
                else -> '.'
            }
        }.joinToString("")
    )
}

fun calculateChecksum(disk: Disk): Long =
    disk.withIndex().sumOf { (idx, diskStatus) ->
        ((diskStatus as? DiskStatus.Filled)?.let {
            idx * it.value
        } ?: 0).toLong()
    }

fun calculateChecksum2(disk: String): Long =
    disk.withIndex().sumOf { (idx, char) ->
        if (char != '.') {
            idx * char.digitToInt().toLong()
        } else {
            0.toLong()
        }
    }

data class Thing(val idx: Int, val numFilled: Int, val numEmpty: Int)

fun List<DiskStatus>.toString2(): String {
    return this.map {
        if (it is DiskStatus.Filled) { it.value } else '.'
    }.joinToString("")
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

fun findConsecutiveBlanks(disk: Disk, numConsecutive: Int): Pair<Int, Int>? {
    for (i in 0..disk.size - numConsecutive) {
        if (disk.subList(i, i + numConsecutive).all { it is DiskStatus.Empty }) {
            return Pair(i, i + numConsecutive)
        }
    }
    return null
}

sealed interface MemoryBlock {
    val size: Int
    val startIdx: Int
    data class Filled(override val size: Int, override var startIdx: Int, val value: Int) : MemoryBlock
    data class Empty(override var size: Int, override var startIdx: Int, ) : MemoryBlock

    fun toString2(): String {
        return when (this) {
            is Filled -> this.value.toString().repeat(this.size)
            else -> '.'.toString().repeat(this.size)
        }
    }
}

enum class Type {
    FILLED,
    EMPTY,
}
data class DiskRepr(val idx: Int, val size: Int, val type: Type)


fun printDisk2(disk: List<MemoryBlock>) {
    disk.forEach {
        print(
            when (it) {
                is MemoryBlock.Filled -> (it.value).toString().repeat(it.size)
                else -> '.'.toString().repeat(it.size)
            }
        )
    }
    println()
    //println()
}

fun findEmptyBlockToLeft(disk: Disk2, requiredSize: Int, maxIdx: Int): Int? {
    val index = disk
        .take(maxIdx)
        .indexOfFirst { it is MemoryBlock.Empty && it.size >= requiredSize }

    return if (index == -1) null else index
}

// region test
//fun Disk2.mergeEmptyBlocks(): Disk2 {
//    //println("Merging: ${this.toStringRepr()}")
//    val newDisk = mutableListOf<MemoryBlock>()
//    var lPtr = 0
//    var rPtr = 0
//    while (rPtr < this.size) {
//        while (lPtr < this.size && this[lPtr] is MemoryBlock.Filled) {
//            //println("Adding l: ${this[lPtr]} - lptr $lPtr")
//            newDisk.add(this[lPtr])
//            lPtr++
//            rPtr = lPtr
//        }
//
//        var emptySize = 0
//        while (rPtr < this.size && this[rPtr] is MemoryBlock.Empty) {
//            emptySize += this[rPtr].size
//            rPtr++
//        }
//
//        //println("Adding empty with size: $emptySize")
//        if (emptySize > 0) {
//            newDisk.add(MemoryBlock.Empty(emptySize))
//        }
//
//        lPtr = rPtr
//    }
//
//    return newDisk
//}

//fun solvePart2(): Long {
//    var disk = mutableListOf<MemoryBlock>()
//    diskMap.chunked(2).map { chunk ->
//        chunk.map { it.digitToInt() }
//    }.forEachIndexed { idx, digits ->
//        val numFilled = digits.first()
//        disk.add(
//            MemoryBlock.Filled(numFilled, idx)
//        )
//        val numEmpty = if (digits.size == 2) digits.last() else 0
//        if (numEmpty > 0) {
//            disk.add(
//                MemoryBlock.Empty(numEmpty)
//            )
//        }
//    }
//
//    for (idx in disk.size - 1 downTo 0) {
//        disk = disk.mergeEmptyBlocks().toMutableList()
//
//        disk.zipWithNext().forEach { (a, b) ->
//            if (a is MemoryBlock.Empty && b is MemoryBlock.Empty) {
//                println("FOK")
//            }
//        }
//        //println("disk after ${disk.toStringRepr()}")
//        val memoryBlock = disk[idx]
//        //println("Looking at $idx")
//        //printDisk2(disk)
//        if (memoryBlock is MemoryBlock.Filled) {
//            //println("Found memory block ${memoryBlock.value}")
//            val emptyBlockIdx = findEmptyBlockToLeft(disk, memoryBlock.size, idx)
//            if (emptyBlockIdx == -1) continue
//            //println("Found space for ${memoryBlock.value} -> ${disk[emptyBlockIdx]} (idx $emptyBlockIdx)")
//            //println("Need to swap ${memoryBlock.value} with ${disk[emptyBlockIdx]}")
//            val emptyBlock = disk[emptyBlockIdx]
//            val sizeDiff = emptyBlock.size - memoryBlock.size
//            disk[emptyBlockIdx] = MemoryBlock.Filled(memoryBlock.size, memoryBlock.value)
//            disk[idx] = MemoryBlock.Empty(memoryBlock.size)
//            if (sizeDiff > 0) {
//                disk.add(emptyBlockIdx + 1, MemoryBlock.Empty(sizeDiff))
//            }
//        }
//    }
//
//    return calculateChecksum2(disk.toStringRepr())
//}

//fun solvePart2Attempt3(): Long {
//    val fileDisk = mutableListOf<MemoryBlock.Filled>()
//    val spaceDisk = mutableListOf<MemoryBlock.Empty>()
//    var startIdx = 0
//    diskMap.chunked(2).map { chunk ->
//        chunk.map { it.digitToInt() }
//    }.forEachIndexed { idx, digits ->
//        val numFilled = digits.first()
//        fileDisk.add(MemoryBlock.Filled(numFilled, startIdx, idx))
//        startIdx += numFilled
//        val numEmpty = if (digits.size == 2) digits.last() else 0
//        if (numEmpty > 0) {
//            spaceDisk.add(
//                MemoryBlock.Empty(numEmpty, startIdx)
//            )
//            startIdx += numEmpty
//        }
//    }
//
//    val newFileDisk = mutableListOf<MemoryBlock.Filled>()
//    fileDisk.reversed().forEach { file ->
//        var fileStart = file.startIdx
//        for ((idx, space) in spaceDisk.withIndex()) {
//            if (file.startIdx < space.startIdx) break
//
//            if (file.size <= space.size) {
//                fileStart = space.startIdx
//                val spaceStart = space.startIdx + file.size
//                val spaceLen = space.size - file.size
//                spaceDisk[idx] = MemoryBlock.Empty(spaceLen, spaceStart)
//                break
//            }
//        }
//        newFileDisk.add(MemoryBlock.Filled(file.size, fileStart, file.value))
//    }
//
//    var ans = 0L
//    for (f in newFileDisk) {
//        for (i in 0..<f.size) {
//            ans += f.value * (f.startIdx + i)
//        }
//    }
//    return ans
//
//}
//
// endregion

//fun solvePart2Attempt3Version2(): Long {
//    val disk = mutableListOf<MemoryBlock>()
//    diskMap.chunked(2).map { chunk ->
//        chunk.map { it.digitToInt() }
//    }.forEachIndexed { idx, digits ->
//        val numFilled = digits.first()
//        disk.add(MemoryBlock.Filled(numFilled, idx))
//        val numEmpty = if (digits.size == 2) digits.last() else 0
//        if (numEmpty > 0) {
//            disk.add(
//                MemoryBlock.Empty(numEmpty)
//            )
//        }
//    }
//    for (d in disk) {
//        println(d)
//    }
//    println()
//
//    val seen = mutableSetOf<Int>()
//    var idx = disk.lastIndex
//    while (idx > 0) {
//    //for (idx in disk.lastIndex downTo 0) {
//        val memoryBlock = disk[idx]
//        //println("memory block: $memoryBlock")
//        if (memoryBlock is MemoryBlock.Empty || (memoryBlock is MemoryBlock.Filled && memoryBlock.value in seen)) {
//            println("Continue")
//            idx--
//            continue
//        }
//        require(memoryBlock is MemoryBlock.Filled)
//        seen.add(memoryBlock.value)
//
//        println("Looking at block $memoryBlock")
//        //printDisk2(disk)
//        val emptyBlockIdx = findEmptyBlockToLeft(
//            disk = disk,
//            requiredSize = memoryBlock.size,
//            maxIdx = idx,
//        )
//        print("Finding space to left of ${idx}... ")
//        if (emptyBlockIdx == null) {
//            println("No space found. Continuing")
//            println()
//            idx--
//            continue
//        }
//
//        println("Found ${disk[emptyBlockIdx]} (idx $emptyBlockIdx)")
//        val emptyBlock = disk[emptyBlockIdx]
//        val sizeDiff = emptyBlock.size - memoryBlock.size
//        disk[emptyBlockIdx] = memoryBlock
//        disk[idx] = MemoryBlock.Empty(memoryBlock.size)
//        if (sizeDiff > 0) {
//            disk.add(emptyBlockIdx + 1, MemoryBlock.Empty(sizeDiff))
//            idx++
//        }
//
//        idx--
//
//        println()
//    }
//
//    val diskStr = disk.toStringRepr()
//    //println(diskStr)
//    return calculateChecksum2(diskStr)
//}

fun findEmptyBlockToLeft2(disk: List<Char>, requiredSize: Int, maxIdx: Int): Int? {
    for (i in 0..maxIdx - requiredSize) {
        if (disk.subList(i, i + requiredSize).all { it == '.' }) {
            return i
        }
    }
    return null
}

fun solvePart2Attempt4(): Long {
    val seen = mutableSetOf<Char>()
    val diskChars = mutableListOf<Char>()
    diskMap.chunked(2).map { chunk ->
        chunk.map { it.digitToInt() }
    }.forEachIndexed { idx, digits ->
        val numFilled = digits.first()
        //diskStr += idx.toString().repeat(numFilled)
        diskChars.addAll(idx.toString().repeat(numFilled).toList())
        val numEmpty = if (digits.size == 2) digits.last() else 0
        if (numEmpty > 0) {
            diskChars.addAll(".".repeat(numEmpty).toList())
        }
    }

    //println(diskChars.joinToString(""))
    var endIdx = diskChars.lastIndex
    var f = false
    while (endIdx >= 0) {
        val currChar = diskChars[endIdx]
        while (endIdx >= 0 && diskChars[endIdx] == '.') {
            endIdx--
            f = true
        }
        if (f) {
            f = false
            continue
        }

        var startIdx = endIdx

        while (startIdx >= 0 && diskChars[startIdx] == currChar) {
            startIdx--
        }

        val memoryBlockStart = startIdx + 1
        val memoryBlockEnd = endIdx
        val memoryBlockSize = (memoryBlockEnd - memoryBlockStart) + 1

        // Find first block where this will fit
        val emptyBlockStartIdx = findEmptyBlockToLeft2(diskChars, memoryBlockSize, startIdx)
        //println("Character '$currChar' ($memoryBlockSize) --- fits $emptyBlockStartIdx")
        if (currChar in seen) {
            endIdx = startIdx
            continue
        }
        seen.add(currChar)
        if (emptyBlockStartIdx == null) {
            endIdx = startIdx
            continue
        }

        //println("Swapping")
        //println(diskChars.joinToString(""))
        diskChars.subList(emptyBlockStartIdx, emptyBlockStartIdx + memoryBlockSize).fill(currChar)
        diskChars.subList(memoryBlockStart, memoryBlockEnd + 1).fill('.')
        //println(diskChars.joinToString(""))
        //println()

        // Move to the next run to the left
        endIdx = startIdx
    }

    return calculateChecksum2(diskChars.joinToString(""))
}


fun p(files: List<MemoryBlock.Filled>, spaces: List<MemoryBlock.Empty>) {
    val disk = buildList {
        addAll(files)
        addAll(spaces)
    }.sortedBy { it.startIdx }
    println(disk.toStringRepr())
}

fun solvePart2Attempt5(): Long {
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

    p(files, spaces)
    val movedFiles = mutableListOf<MemoryBlock.Filled>()
    for (fileIdx in files.lastIndex downTo 0) {
        val file = files[fileIdx]
        println()
        println("File: $file")
        //p(files, spaces)
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
        println("Found space: $emptySpace (at index $emptySpaceStartIdx)")

        val actualStart = emptySpace.startIdx

        spaces[emptySpaceStartIdx].startIdx += file.size
        spaces[emptySpaceStartIdx].size -= file.size
        // Need to use the original start index
        files[fileIdx].startIdx = actualStart

        movedFiles.add(MemoryBlock.Filled(file.size, actualStart, file.value))
        //p(movedFiles, spaces)

        println()
    }

    //files.reversed().forEach { file ->
    //    var fileStart = file.startIdx
    //    for ((idx, space) in spaces.withIndex()) {
    //        if (file.startIdx < space.startIdx) break
    //
    //        if (file.size <= space.size) {
    //            fileStart = space.startIdx
    //            val spaceStart = space.startIdx + file.size
    //            val spaceLen = space.size - file.size
    //            spaces[idx] = MemoryBlock.Empty(spaceLen, spaceStart)
    //            break
    //        }
    //    }
    //    movedFiles.add(MemoryBlock.Filled(file.size, fileStart, file.value))
    //}

    var ans = 0L
    for (f in movedFiles) {
        for (i in 0..<f.size) {
            ans += f.value * (f.startIdx + i)
        }
    }
    return ans
}


println("Part 1 answer: ${solvePart1()}")
//println("Part 2 answer: ${solvePart2()}")
//println("Part 2 answer: ${solvePart2Attempt3()}")
//println("Part 2 answer: ${solvePart2Attempt3Version2()}")
//println("Part 2 answer: ${solvePart2Attempt4()}")
println("Part 2 answer: ${solvePart2Attempt5()}")
