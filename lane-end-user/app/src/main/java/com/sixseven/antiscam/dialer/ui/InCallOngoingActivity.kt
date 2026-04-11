package com.sixseven.antiscam.dialer.ui

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.os.SystemClock
import android.telecom.Call
import android.view.View
import android.widget.Button
import android.widget.Chronometer
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.sixseven.antiscam.R
import com.sixseven.antiscam.dialer.call.ActiveCallStore
import com.sixseven.antiscam.dialer.call.CallControlFacade
import com.sixseven.antiscam.dialer.call.FallbackRingingStore

class InCallOngoingActivity : AppCompatActivity() {

    private lateinit var callerText: TextView
    private lateinit var stateText: TextView
    private lateinit var durationChronometer: Chronometer
    private lateinit var muteButton: Button
    private lateinit var speakerButton: Button
    private lateinit var endButton: Button

    private var observedCall: Call? = null
    private var timerStarted = false
    private var isMuted = false
    private var isSpeakerOn = false

    private val callCallback = object : Call.Callback() {
        override fun onStateChanged(call: Call, state: Int) {
            runOnUiThread {
                renderState(state)
                if (state == Call.STATE_DISCONNECTED) {
                    finish()
                }
            }
        }

        override fun onDetailsChanged(call: Call, details: Call.Details) {
            runOnUiThread {
                callerText.text = details.handle?.schemeSpecificPart.orEmpty().ifBlank {
                    FallbackRingingStore.currentLabel()
                }
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_in_call_ongoing)

        bindViews()
        bindActions()
    }

    override fun onStart() {
        super.onStart()
        attachCurrentCall()
    }

    override fun onStop() {
        runCatching { observedCall?.unregisterCallback(callCallback) }
        observedCall = null
        super.onStop()
    }

    private fun bindViews() {
        callerText = findViewById(R.id.tvOngoingCaller)
        stateText = findViewById(R.id.tvOngoingState)
        durationChronometer = findViewById(R.id.chronometerCall)
        muteButton = findViewById(R.id.btnMute)
        speakerButton = findViewById(R.id.btnSpeaker)
        endButton = findViewById(R.id.btnEndCall)
    }

    private fun bindActions() {
        endButton.setOnClickListener {
            CallControlFacade.end(this)
            finish()
        }

        muteButton.setOnClickListener {
            isMuted = !isMuted
            muteButton.text = if (isMuted) "Muted" else "Mute"
        }

        speakerButton.setOnClickListener {
            isSpeakerOn = !isSpeakerOn
            speakerButton.text = if (isSpeakerOn) "Speaker ON" else "Speaker"
        }
    }

    private fun attachCurrentCall() {
        val call = ActiveCallStore.current()
        if (call == null) {
            finish()
            return
        }

        if (call.state == Call.STATE_RINGING) {
            startActivity(IncomingCallActivity.buildIntent(this))
            finish()
            return
        }

        runCatching { observedCall?.unregisterCallback(callCallback) }
        observedCall = call
        runCatching { observedCall?.registerCallback(callCallback) }

        callerText.text = runCatching {
            call.details.handle?.schemeSpecificPart.orEmpty()
        }.getOrDefault("").ifBlank {
            FallbackRingingStore.currentLabel()
        }

        val safeState = runCatching { call.state }.getOrDefault(Call.STATE_ACTIVE)
        renderState(safeState)
    }

    private fun renderState(state: Int) {
        when (state) {
            Call.STATE_ACTIVE -> {
                stateText.text = "Call in progress"
                durationChronometer.visibility = View.VISIBLE
                if (!timerStarted) {
                    durationChronometer.base = SystemClock.elapsedRealtime()
                    durationChronometer.start()
                    timerStarted = true
                }
            }

            Call.STATE_CONNECTING,
            Call.STATE_DIALING -> {
                stateText.text = "Connecting..."
            }

            Call.STATE_DISCONNECTED -> {
                durationChronometer.stop()
                finish()
            }

            else -> {
                stateText.text = "Call in progress"
            }
        }
    }

    companion object {
        fun buildIntent(context: Context): Intent {
            return Intent(context, InCallOngoingActivity::class.java).apply {
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP)
                addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP)
            }
        }
    }
}
