package com.sixseven.antiscam.dialer.call

import android.telecom.Call
import android.telecom.VideoProfile

object ActiveCallStore {

    private var currentCall: Call? = null

    @Synchronized
    fun attach(call: Call) {
        currentCall = call
    }

    @Synchronized
    fun current(): Call? = currentCall

    @Synchronized
    fun clear(call: Call? = null) {
        if (call == null || currentCall === call) {
            currentCall = null
        }
    }

    @Synchronized
    fun answer() {
        try {
            currentCall?.answer(VideoProfile.STATE_AUDIO_ONLY)
        } catch (_: Throwable) {
            // Ignored: can fail if role/permissions are revoked while app is running.
        }
    }

    @Synchronized
    fun decline() {
        try {
            currentCall?.reject(false, null)
        } catch (_: Throwable) {
            // Ignored: can fail if role/permissions are revoked while app is running.
        }
    }

    @Synchronized
    fun end() {
        try {
            currentCall?.disconnect()
        } catch (_: Throwable) {
            // Ignored: can fail if role/permissions are revoked while app is running.
        }
    }
}
