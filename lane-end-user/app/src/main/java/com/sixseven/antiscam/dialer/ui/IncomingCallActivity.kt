package com.sixseven.antiscam.dialer.ui

import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.Bundle
import android.telecom.Call
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.view.WindowManager
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.updatePadding
import com.sixseven.antiscam.R
import com.sixseven.antiscam.dialer.call.ActiveCallStore
import com.sixseven.antiscam.dialer.call.CallControlFacade
import com.sixseven.antiscam.dialer.call.FallbackRingingStore
import com.sixseven.antiscam.dialer.debug.IncomingDebugReporter

class IncomingCallActivity : AppCompatActivity() {

    private lateinit var callerTitle: TextView
    private lateinit var callStateText: TextView
    private lateinit var answerButton: TextView
    private lateinit var declineButton: TextView

    private var observedCall: Call? = null
    private var openedOngoingScreen = false

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
                updateCaller(details.handle?.schemeSpecificPart.orEmpty())
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_incoming_call)

        setupWindowAsTopBanner()
        applyStatusBarInsets()
        setupLockScreenBehavior()
        bindViews()
        bindActions()
        FallbackRingingStore.markUiDisplayed()
        IncomingDebugReporter.report(
            event = "incoming_activity_created",
            details = mapOf(
                "fallbackLabel" to FallbackRingingStore.currentLabel(),
                "hasActiveCall" to (ActiveCallStore.current() != null)
            )
        )
    }

    override fun onStart() {
        super.onStart()
        IncomingDebugReporter.report(
            event = "incoming_activity_started",
            details = mapOf(
                "hasActiveCall" to (ActiveCallStore.current() != null),
                "isFallbackRinging" to FallbackRingingStore.isRinging()
            )
        )
        attachCurrentCall()
    }

    override fun onStop() {
        runCatching { observedCall?.unregisterCallback(callCallback) }
        observedCall = null
        super.onStop()
    }

    private fun bindViews() {
        callerTitle = findViewById(R.id.tvCaller)
        callStateText = findViewById(R.id.tvCallState)
        answerButton = findViewById(R.id.btnAnswerCall)
        declineButton = findViewById(R.id.btnDeclineCall)
    }

    private fun bindActions() {
        answerButton.setOnClickListener {
            val answered = CallControlFacade.answer(this)
            if (!answered) {
                Toast.makeText(this, "Cannot answer call. Check Phone permissions.", Toast.LENGTH_SHORT)
                    .show()
                return@setOnClickListener
            }

            openOngoingCallScreen()
            finish()
        }

        declineButton.setOnClickListener {
            val current = ActiveCallStore.current()
            val currentState = runCatching { current?.state }.getOrNull()
            val declined = if (currentState == Call.STATE_RINGING) {
                CallControlFacade.decline(this)
            } else {
                CallControlFacade.end(this)
            }

            if (!declined) {
                Toast.makeText(this, "Cannot decline call. Please try again.", Toast.LENGTH_SHORT)
                    .show()
                return@setOnClickListener
            }

            finish()
        }
    }

    private fun attachCurrentCall() {
        val call = ActiveCallStore.current()
        if (call == null && !FallbackRingingStore.isRinging()) {
            finish()
            return
        }

        if (call == null) {
            updateCaller(FallbackRingingStore.currentLabel())
            renderState(Call.STATE_RINGING)
            return
        }

        observedCall?.unregisterCallback(callCallback)
        observedCall = call
        runCatching { observedCall?.registerCallback(callCallback) }

        val safeCaller = runCatching { call.details.handle?.schemeSpecificPart.orEmpty() }
            .getOrDefault(FallbackRingingStore.currentLabel())
        val safeState = runCatching { call.state }.getOrDefault(Call.STATE_RINGING)

        updateCaller(safeCaller)
        renderState(safeState)
    }

    private fun updateCaller(rawCaller: String) {
        callerTitle.text = rawCaller.ifBlank { "Unknown caller" }
    }

    private fun renderState(state: Int) {
        when (state) {
            Call.STATE_RINGING -> {
                callStateText.text = "Đang gọi đến"
                answerButton.visibility = View.VISIBLE
            }

            Call.STATE_ACTIVE -> {
                callStateText.text = "Đang trong cuộc gọi"
                answerButton.visibility = View.GONE
                openOngoingCallScreen()
            }

            Call.STATE_CONNECTING,
            Call.STATE_DIALING -> {
                callStateText.text = "Đang kết nối..."
                answerButton.visibility = View.GONE
            }

            Call.STATE_DISCONNECTED -> {
                finish()
            }

            else -> {
                callStateText.text = "Đang xử lý..."
            }
        }
    }

    private fun setupLockScreenBehavior() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O_MR1) {
            setShowWhenLocked(true)
            setTurnScreenOn(true)
        } else {
            @Suppress("DEPRECATION")
            window.addFlags(
                WindowManager.LayoutParams.FLAG_SHOW_WHEN_LOCKED or
                    WindowManager.LayoutParams.FLAG_TURN_SCREEN_ON
            )
        }
    }

    private fun setupWindowAsTopBanner() {
        window.setLayout(
            ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.WRAP_CONTENT
        )
        window.setGravity(Gravity.TOP)
        window.clearFlags(WindowManager.LayoutParams.FLAG_DIM_BEHIND)
    }

    private fun applyStatusBarInsets() {
        val root = findViewById<View>(R.id.rootIncomingCall)
        val baseTopPadding = root.paddingTop

        ViewCompat.setOnApplyWindowInsetsListener(root) { view, insets ->
            val topInset = insets.getInsets(WindowInsetsCompat.Type.statusBars()).top
            view.updatePadding(top = baseTopPadding + topInset)
            insets
        }

        ViewCompat.requestApplyInsets(root)
    }

    private fun openOngoingCallScreen() {
        if (openedOngoingScreen) {
            return
        }

        openedOngoingScreen = true
        startActivity(InCallOngoingActivity.buildIntent(this))
    }

    companion object {
        fun buildIntent(context: Context): Intent {
            return Intent(context, IncomingCallActivity::class.java).apply {
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP)
                addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP)
            }
        }
    }
}
