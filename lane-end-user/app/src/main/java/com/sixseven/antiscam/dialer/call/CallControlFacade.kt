package com.sixseven.antiscam.dialer.call

import android.content.Context
import android.os.Build
import android.telecom.Call
import android.telecom.TelecomManager

object CallControlFacade {

    fun answer(context: Context): Boolean {
        val current = ActiveCallStore.current()
        if (current != null) {
            ActiveCallStore.answer()
            return true
        }

        val telecomManager = context.getSystemService(TelecomManager::class.java) ?: return false
        return try {
            telecomManager.acceptRingingCall()
            FallbackRingingStore.onCallEndedOrPicked()
            true
        } catch (_: Throwable) {
            false
        }
    }

    fun decline(context: Context): Boolean {
        val current = ActiveCallStore.current()
        if (current != null) {
            ActiveCallStore.decline()
            return true
        }

        val telecomManager = context.getSystemService(TelecomManager::class.java) ?: return false
        return try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                telecomManager.silenceRinger()
            }
            FallbackRingingStore.onCallEndedOrPicked()
            true
        } catch (_: Throwable) {
            false
        }
    }

    fun end(context: Context): Boolean {
        val current = ActiveCallStore.current()
        if (current?.state == Call.STATE_ACTIVE || current?.state == Call.STATE_DIALING) {
            ActiveCallStore.end()
            return true
        }

        return false
    }
}
