package com.fusehark.timeline

import java.io.File

/**
 * M1: append-only segment registry (Room lands in M2; file index proves the loop).
 */
class TimelineStore(private val root: File) {
    private val index = File(root, "segments/index.txt").apply {
        parentFile?.mkdirs()
    }

    fun registerSegment(name: String, bytes: Long) {
        index.appendText("$name|$bytes|${System.currentTimeMillis()}\n")
    }

    fun listSegments(): List<String> =
        if (index.exists()) index.readLines().filter { it.isNotBlank() } else emptyList()
}
