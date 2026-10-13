package com.fusehark.capture

import android.Manifest
import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Intent
import android.content.pm.PackageManager
import android.media.AudioFormat
import android.media.AudioRecord
import android.media.MediaRecorder
import android.os.IBinder
import androidx.core.app.ActivityCompat
import java.io.File
import java.io.FileOutputStream
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import kotlin.concurrent.thread

/**
 * M1: foreground mic capture -> 16kHz/16-bit/mono WAV segments on disk.
 * Consent banner = persistent notification. No ML deps (VAD/STT land in M2).
 */
class AudioCaptureService : Service() {

    companion object {
        const val SAMPLE_RATE = 16000
        const val CHANNEL = AudioFormat.CHANNEL_IN_MONO
        const val ENCODING = AudioFormat.ENCODING_PCM_16BIT
        const val SEGMENT_SECONDS = 30
        const val CHANNEL_ID = "fusehark_capture"
    }

    @Volatile private var running = false
    private var worker: Thread? = null

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        val nm = getSystemService(NotificationManager::class.java)
        nm.createNotificationChannel(
            NotificationChannel(CHANNEL_ID, "FuseHark listening",
                NotificationManager.IMPORTANCE_LOW)
        )
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)
            != PackageManager.PERMISSION_GRANTED) {
            stopSelf()
            return START_NOT_STICKY
        }
        val note = Notification.Builder(this, CHANNEL_ID)
            .setContentTitle("FuseHark is listening")
            .setContentText("Tap to open. Stop anytime — consent first.")
            .setSmallIcon(android.R.drawable.ic_btn_speak_now)
            .build()
        startForeground(1, note)
        if (!running) {
            running = true
            worker = thread(name = "fusehark-capture", isDaemon = true) { loop() }
        }
        return START_STICKY
    }

    override fun onDestroy() {
        running = false
        worker?.join(2000)
        super.onDestroy()
    }

    private fun loop() {
        val minBuf = AudioRecord.getMinBufferSize(
            SAMPLE_RATE, CHANNEL, ENCODING).coerceAtLeast(4096)
        val rec = AudioRecord(
            MediaRecorder.AudioSource.VOICE_RECOGNITION,
            SAMPLE_RATE, CHANNEL, ENCODING, minBuf * 4)
        if (rec.state != AudioRecord.STATE_INITIALIZED) {
            running = false
            stopSelf()
            return
        }
        val dir = File(filesDir, "segments").apply { mkdirs() }
        val stamp = SimpleDateFormat("yyyyMMdd-HHmmss", Locale.US).format(Date())
        val out = File(dir, "seg-$stamp.pcm")
        rec.startRecording()
        FileOutputStream(out).use { fos ->
            val buf = ByteArray(minBuf)
            val endAt = System.currentTimeMillis() + SEGMENT_SECONDS * 1000L
            while (running && System.currentTimeMillis() < endAt) {
                val n = rec.read(buf, 0, buf.size)
                if (n > 0) fos.write(buf, 0, n)
            }
        }
        runCatching { rec.stop() }
        rec.release()
        running = false
        stopSelf()
    }
}
