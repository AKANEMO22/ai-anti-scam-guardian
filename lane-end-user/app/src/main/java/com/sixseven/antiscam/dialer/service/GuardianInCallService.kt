package com.sixseven.antiscam.dialer.service

import android.telecom.Call
import android.telecom.InCallService
import com.sixseven.antiscam.dialer.call.ActiveCallStore
import com.sixseven.antiscam.dialer.call.FallbackRingingStore
import com.sixseven.antiscam.dialer.debug.IncomingDebugReporter
import com.sixseven.antiscam.dialer.ui.CallNotificationController

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
        IncomingDebugReporter.report(
            event = "incall_service_call_added",
            details = mapOf(
                "state" to runCatching { call.state }.getOrDefault(-1)
            )
        )
        runCatching {
            call.registerCallback(callCallback)
            handleStateUpdate(call, call.state)
        }
    }

    override fun onCallRemoved(call: Call) {
        runCatching { call.unregisterCallback(callCallback) }
        ActiveCallStore.clear(call)
        CallNotificationController.cancel(this)
        IncomingDebugReporter.report(
            event = "incall_service_call_removed",
            details = mapOf(
                "state" to runCatching { call.state }.getOrDefault(-1)
            )
        )
        super.onCallRemoved(call)
    }

    private fun handleStateUpdate(call: Call, state: Int) {
        when (state) {
            Call.STATE_RINGING -> {
                val caller = resolveCallerLabel(call)
                FallbackRingingStore.onRinging(caller)
                IncomingDebugReporter.report(
                    event = "incall_state_ringing",
                    details = mapOf(
                        "callerLabel" to caller,
                        "notificationMode" to "call_style"
                    )
                )
                CallNotificationController.showIncomingCall(
                    context = this,
                    callerLabel = FallbackRingingStore.currentLabel()
                )
            }

            Call.STATE_ACTIVE,
            Call.STATE_CONNECTING,
            Call.STATE_DIALING -> {
                FallbackRingingStore.onCallEndedOrPicked()
                CallNotificationController.cancel(this)
                IncomingDebugReporter.report(
                    event = "incall_state_connected",
                    details = mapOf("state" to state)
                )
            }

            Call.STATE_DISCONNECTED -> {
                ActiveCallStore.clear(call)
                FallbackRingingStore.onCallEndedOrPicked()
                CallNotificationController.cancel(this)
                IncomingDebugReporter.report(
                    event = "incall_state_disconnected",
                    details = mapOf("state" to state)
                )
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
