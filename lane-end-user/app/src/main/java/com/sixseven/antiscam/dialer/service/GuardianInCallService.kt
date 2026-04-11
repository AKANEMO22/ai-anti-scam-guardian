package com.sixseven.antiscam.dialer.service

import android.telecom.Call
import android.telecom.InCallService
import com.sixseven.antiscam.dialer.call.ActiveCallStore
import com.sixseven.antiscam.dialer.call.FallbackRingingStore
import com.sixseven.antiscam.dialer.ui.CallNotificationController
import com.sixseven.antiscam.dialer.ui.IncomingCallActivity

class GuardianInCallService : InCallService() {

    private val callCallback = object : Call.Callback() {
        override fun onStateChanged(call: Call, state: Int) {
            handleStateUpdate(call, state)
        }
    }

    override fun onCallAdded(call: Call) {
        super.onCallAdded(call)
        ActiveCallStore.attach(call)
        CallNotificationController.cancel(this)
        runCatching {
            call.registerCallback(callCallback)
            handleStateUpdate(call, call.state)
        }
    }

    override fun onCallRemoved(call: Call) {
        runCatching { call.unregisterCallback(callCallback) }
        ActiveCallStore.clear(call)
        CallNotificationController.cancel(this)
        super.onCallRemoved(call)
    }

    private fun handleStateUpdate(call: Call, state: Int) {
        when (state) {
            Call.STATE_RINGING -> {
                val caller = resolveCallerLabel(call)
                FallbackRingingStore.onRinging(caller)
                CallNotificationController.showIncomingCall(this, FallbackRingingStore.currentLabel())
                runCatching {
                    startActivity(IncomingCallActivity.buildIntent(this))
                }
            }

            Call.STATE_ACTIVE,
            Call.STATE_CONNECTING,
            Call.STATE_DIALING -> {
                FallbackRingingStore.onCallEndedOrPicked()
                CallNotificationController.cancel(this)
            }

            Call.STATE_DISCONNECTED -> {
                ActiveCallStore.clear(call)
                FallbackRingingStore.onCallEndedOrPicked()
                CallNotificationController.cancel(this)
            }
        }
    }

    private fun resolveCallerLabel(call: Call): String {
        val rawHandle = runCatching {
            call.details.handle?.schemeSpecificPart.orEmpty().trim()
        }.getOrDefault("")
        return if (rawHandle.isNotBlank()) {
            rawHandle
        } else {
            "Unknown caller"
        }
    }
}
