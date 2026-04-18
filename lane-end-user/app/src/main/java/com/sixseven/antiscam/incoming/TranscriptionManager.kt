package com.sixseven.antiscam.incoming

import android.Manifest
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.util.Log
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import androidx.core.content.ContextCompat

class TranscriptionManager(private val context: Context) {
    private var speechRecognizer: SpeechRecognizer? = null
    private var sttIntent: Intent? = null
    private var handler: Handler = Handler(Looper.getMainLooper())
    private var active = false
    private var errorCount = 0
    private val MAX_ERROR_RETRIES = 8
    private val BASE_RETRY_MS = 250L
    private val MAX_RETRY_MS = 5_000L

    // Debounce outgoing status broadcasts to avoid rapid UI flicker
    private var statusDebounceRunnable: Runnable? = null
    private var lastBroadcastedCapturing: Boolean? = null
    private val STATUS_DEBOUNCE_MS = 600L

    private fun broadcastStatus(capturing: Boolean, message: String? = null, immediate: Boolean = false) {
        // If immediate requested, cancel any pending debounce and send now
        if (immediate) {
            statusDebounceRunnable?.let { handler.removeCallbacks(it) }
            statusDebounceRunnable = null
            val intent = Intent(IncomingCallContracts.ACTION_TRANSCRIPTION_STATUS).apply {
                setPackage(context.packageName)
                putExtra(IncomingCallContracts.EXTRA_TRANSCRIPTION_CAPTURING, capturing)
                if (message != null) putExtra(IncomingCallContracts.EXTRA_TRANSCRIPTION_STATUS_MESSAGE, message)
            }
            context.sendBroadcast(intent)
            lastBroadcastedCapturing = capturing
            return
        }

        // Debounced send: only send after STATUS_DEBOUNCE_MS without flip-flop
        statusDebounceRunnable?.let { handler.removeCallbacks(it) }
        val runnable = Runnable {
            // send when changed or if there's a status message
            if (lastBroadcastedCapturing == null || lastBroadcastedCapturing != capturing || message != null) {
                val intent = Intent(IncomingCallContracts.ACTION_TRANSCRIPTION_STATUS).apply {
                    setPackage(context.packageName)
                    putExtra(IncomingCallContracts.EXTRA_TRANSCRIPTION_CAPTURING, capturing)
                    if (message != null) putExtra(IncomingCallContracts.EXTRA_TRANSCRIPTION_STATUS_MESSAGE, message)
                }
                context.sendBroadcast(intent)
                lastBroadcastedCapturing = capturing
            }
            statusDebounceRunnable = null
        }
        statusDebounceRunnable = runnable
        handler.postDelayed(runnable, STATUS_DEBOUNCE_MS)
    }

    fun start() {
        if (active) return
        if (ContextCompat.checkSelfPermission(context, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            broadcastError("Missing RECORD_AUDIO permission")
            return
        }

        sttIntent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
            putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, true)
            putExtra(RecognizerIntent.EXTRA_LANGUAGE, "vi-VN")
            putExtra(RecognizerIntent.EXTRA_CALLING_PACKAGE, context.packageName)
        }

        val sr = runCatching { SpeechRecognizer.createSpeechRecognizer(context) }.getOrNull()
        if (sr == null) {
            Log.w("TranscriptionManager", "SpeechRecognizer not available")
            broadcastError("SpeechRecognizer not available")
            return
        }

        sr.setRecognitionListener(object : RecognitionListener {
            override fun onReadyForSpeech(params: Bundle?) {}
            override fun onBeginningOfSpeech() {}
            override fun onRmsChanged(rmsdB: Float) {}
            override fun onBufferReceived(buffer: ByteArray?) {}
            override fun onEndOfSpeech() {}

            override fun onError(error: Int) {
                // incremental backoff on repeated errors to avoid rapid restart cycles
                errorCount = (errorCount + 1).coerceAtLeast(1)
                val backoff = (BASE_RETRY_MS * (1L shl (errorCount - 1))).coerceAtMost(MAX_RETRY_MS)
                Log.w("TranscriptionManager", "STT onError code=$error retry=$errorCount backoff=${backoff}ms")

                // notify UI (debounced)
                broadcastStatus(false, "error_code=$error", immediate = false)

                if (errorCount >= MAX_ERROR_RETRIES) {
                    Log.w("TranscriptionManager", "STT failing repeatedly - pausing retries")
                    broadcastError("STT failing repeatedly (" + errorCount + ")")
                    stop()
                    return
                }

                handler.postDelayed({ restart() }, backoff)
            }

            override fun onResults(results: Bundle?) {
                val matches = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                val text = matches?.firstOrNull().orEmpty()
                // successful final result -> reset error counter and broadcast
                errorCount = 0
                broadcastTranscript(text, true)
                handler.postDelayed({ restart() }, 400)
            }

            override fun onPartialResults(partialResults: Bundle?) {
                val partial = partialResults?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)?.firstOrNull().orEmpty()
                // partial results indicate healthy recognition; reset error counter
                errorCount = 0
                broadcastTranscript(partial, false)
            }

            override fun onEvent(eventType: Int, params: Bundle?) {}
        })

        speechRecognizer = sr
        active = true
        Log.d("TranscriptionManager", "STT started")
        try {
            sr.startListening(sttIntent)
            // reset error counter on a successful start attempt
            errorCount = 0
            // notify listeners that STT is actively listening (debounced)
            broadcastStatus(true)
        } catch (e: Exception) {
            Log.w("TranscriptionManager", "STT start failed: ${e.message}")
            broadcastError("STT start failed: ${e.message}")
            stop()
        }
    }

    private fun restart() {
        if (!active) return
        stop()
        handler.postDelayed({ start() }, 200)
    }

    fun stop() {
        // clear pending callbacks but keep other app callbacks safe
        handler.removeCallbacksAndMessages(null)
        runCatching { speechRecognizer?.stopListening() }
        runCatching { speechRecognizer?.cancel() }
        runCatching { speechRecognizer?.destroy() }
        speechRecognizer = null
        sttIntent = null
        active = false
        Log.d("TranscriptionManager", "STT stopped")
        // broadcast stop immediately so UI doesn't linger in green state
        broadcastStatus(false, "STT stopped", immediate = true)
        // reset error counter for next start
        errorCount = 0
    }

    private fun broadcastTranscript(text: String, isFinal: Boolean) {
        TranscriptionStore.latest = text
        Log.d("TranscriptionManager", "broadcastTranscript final=${isFinal} text=${text.take(200)}")
        val intent = Intent(IncomingCallContracts.ACTION_TRANSCRIPTION_UPDATED).apply {
            setPackage(context.packageName)
            putExtra(IncomingCallContracts.EXTRA_TRANSCRIPT_TEXT, text)
            putExtra(IncomingCallContracts.EXTRA_TRANSCRIPT_IS_FINAL, isFinal)
        }
        context.sendBroadcast(intent)
    }

    private fun broadcastError(message: String) {
        Log.w("TranscriptionManager", "broadcastError: $message")
        val intent = Intent(IncomingCallContracts.ACTION_TRANSCRIPTION_ERROR).apply {
            setPackage(context.packageName)
            putExtra(IncomingCallContracts.EXTRA_TRANSCRIPTION_ERROR, message)
        }
        context.sendBroadcast(intent)
        // Also emit status=false immediately so UI can update without debounce
        broadcastStatus(false, message, immediate = true)
    }
}
