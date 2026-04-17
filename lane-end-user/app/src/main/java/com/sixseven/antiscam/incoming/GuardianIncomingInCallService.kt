package com.sixseven.antiscam.incoming

import android.content.Intent
import android.telecom.Call
import android.telecom.CallAudioState
import android.telecom.InCallService
import android.telephony.TelephonyManager

class GuardianIncomingInCallService : InCallService() {

    companion object {
        private val serviceLock = Any()
        private var activeService: GuardianIncomingInCallService? = null

        fun requestSpeakerRoute(enabled: Boolean): Boolean {
            val service = synchronized(serviceLock) { activeService } ?: return false
            return service.applySpeakerRoute(enabled)
        }

        fun isSpeakerRouteEnabled(): Boolean? {
            val service = synchronized(serviceLock) { activeService } ?: return null
            return service.isSpeakerRouteActive()
        }

        fun requestMicrophoneMute(enabled: Boolean): Boolean {
            val service = synchronized(serviceLock) { activeService } ?: return false
            return service.applyMicrophoneMute(enabled)
        }

        fun isMicrophoneMuted(): Boolean? {
            val service = synchronized(serviceLock) { activeService } ?: return null
            return service.isMicrophoneMuteActive()
        }
    }

    private val callCallback = object : Call.Callback() {
        override fun onStateChanged(call: Call, state: Int) {
            handleStateUpdate(call, state)
        }
    }

    override fun onCreate() {
        super.onCreate()
        synchronized(serviceLock) {
            activeService = this
        }
    }

    override fun onDestroy() {
        synchronized(serviceLock) {
            if (activeService === this) {
                activeService = null
            }
        }
        super.onDestroy()
    }

    override fun onCallAdded(call: Call) {
        super.onCallAdded(call)
        IncomingActiveCallStore.attach(call)
        call.registerCallback(callCallback)
        handleStateUpdate(call, call.state)
    }

    override fun onCallRemoved(call: Call) {
        runCatching { call.unregisterCallback(callCallback) }
        IncomingActiveCallStore.clear(call)
        IncomingCallNotifier.cancelIncomingCall(this)
        IncomingCallStateStore.clear()
        broadcastCallState(TelephonyManager.EXTRA_STATE_IDLE, null)
        super.onCallRemoved(call)
    }

    private fun handleStateUpdate(call: Call, state: Int) {
        when (state) {
            Call.STATE_RINGING -> {
                val caller = resolveCallerLabel(call)
                IncomingCallStateStore.onRinging(caller)
                IncomingCallNotifier.showIncomingCall(this, IncomingCallStateStore.currentLabel())
                broadcastCallState(TelephonyManager.EXTRA_STATE_RINGING, IncomingCallStateStore.currentLabel())
            }

            Call.STATE_ACTIVE,
            Call.STATE_CONNECTING,
            Call.STATE_DIALING -> {
                IncomingCallNotifier.cancelIncomingCall(this)
                broadcastCallState(TelephonyManager.EXTRA_STATE_OFFHOOK, resolveCallerLabel(call))
            }

            Call.STATE_DISCONNECTED -> {
                IncomingActiveCallStore.clear(call)
                IncomingCallNotifier.cancelIncomingCall(this)
                IncomingCallStateStore.clear()
                broadcastCallState(TelephonyManager.EXTRA_STATE_IDLE, null)
            }
        }
    }

    private fun resolveCallerLabel(call: Call): String {
        val rawHandle = runCatching {
            call.details.handle?.schemeSpecificPart.orEmpty().trim()
        }.getOrDefault("")

        return rawHandle
    }

    private fun applySpeakerRoute(enabled: Boolean): Boolean {
        val currentState = callAudioState
        val supportedMask = currentState?.supportedRouteMask ?: 0
        val targetRoute = if (enabled) {
            CallAudioState.ROUTE_SPEAKER
        } else {
            resolveNonSpeakerRoute(supportedMask)
        }

        return runCatching {
            setAudioRoute(targetRoute)
            true
        }.getOrDefault(false)
    }

    private fun isSpeakerRouteActive(): Boolean {
        val route = callAudioState?.route ?: return false
        return route and CallAudioState.ROUTE_SPEAKER != 0
    }

    private fun applyMicrophoneMute(enabled: Boolean): Boolean {
        return runCatching {
            setMuted(enabled)
            true
        }.getOrDefault(false)
    }

    private fun isMicrophoneMuteActive(): Boolean {
        return callAudioState?.isMuted == true
    }

    private fun resolveNonSpeakerRoute(mask: Int): Int {
        if (mask and CallAudioState.ROUTE_EARPIECE != 0) {
            return CallAudioState.ROUTE_EARPIECE
        }
        if (mask and CallAudioState.ROUTE_WIRED_HEADSET != 0) {
            return CallAudioState.ROUTE_WIRED_HEADSET
        }
        if (mask and CallAudioState.ROUTE_BLUETOOTH != 0) {
            return CallAudioState.ROUTE_BLUETOOTH
        }
        return CallAudioState.ROUTE_EARPIECE
    }

    private fun broadcastCallState(state: String, callerLabel: String?) {
        sendBroadcast(
            Intent(IncomingCallContracts.ACTION_CALL_STATE_CHANGED).apply {
                setPackage(packageName)
                putExtra(IncomingCallContracts.EXTRA_CALL_STATE, state)
                putExtra(IncomingCallContracts.EXTRA_CALLER_LABEL, callerLabel)
            }
        )
    }
}
