package com.fusehark

import android.Manifest
import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import androidx.core.app.ActivityCompat
import com.fusehark.capture.AudioCaptureService
import com.fusehark.timeline.TimelineStore

/** M1: one screen — permission gate + start/stop + segment list. */
class MainActivity : Activity() {

    private lateinit var status: TextView
    private lateinit var store: TimelineStore

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        store = TimelineStore(filesDir)
        val layout = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL }
        status = TextView(this).apply { text = "FuseHark M1 — idle" }
        val btn = Button(this).apply { text = "Start 30s capture" }
        btn.setOnClickListener {
            if (ActivityCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)
                != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(
                    this, arrayOf(Manifest.permission.RECORD_AUDIO), 1)
            } else {
                startService(Intent(this, AudioCaptureService::class.java))
                status.text = "FuseHark M1 — recording 30s…"
            }
        }
        layout.addView(status)
        layout.addView(btn)
        setContentView(layout)
    }

    override fun onResume() {
        super.onResume()
        val segs = store.listSegments()
        if (segs.isNotEmpty()) status.text = "Segments: ${segs.size} (latest ${segs.last()})"
    }
}
