package com.sixseven.antiscam.incoming

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.os.Build
import android.telecom.Call
import android.telecom.TelecomManager
import android.telecom.VideoProfile
import android.util.Log
import androidx.core.content.ContextCompat

object IncomingCallControl {
    private const val TAG = "IncomingCallControl"

    fun answer(context: Context): Boolean {
        IncomingActiveCallStore.current()?.let { activeCall ->
            return try {
                activeCall.answer(VideoProfile.STATE_AUDIO_ONLY)
                true
            } catch (exception: SecurityException) {
                Log.w(TAG, "Unable to answer active call", exception)
                false
            } catch (exception: IllegalStateException) {
                Log.w(TAG, "Answer active call failed due to invalid state", exception)
                false
            }
        }

        if (!hasAnswerPermission(context)) {
            return false
        }

        val telecomManager = context.getSystemService(TelecomManager::class.java) ?: return false

        return try {
            telecomManager.acceptRingingCall()
            true
        } catch (exception: SecurityException) {
            Log.w(TAG, "Unable to answer incoming call", exception)
            false
        } catch (exception: IllegalStateException) {
            Log.w(TAG, "Answer call failed due to invalid state", exception)
            false
        }
    }

    fun decline(context: Context): Boolean {
        IncomingActiveCallStore.current()?.let { activeCall ->
            val state = runCatching { activeCall.state }.getOrDefault(Call.STATE_NEW)
            return if (state == Call.STATE_RINGING) {
                rejectCall(activeCall)
            } else {
                disconnectCall(activeCall)
            }
        }

        if (!hasAnswerPermission(context)) {
            return false
        }

        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.P) {
            return false
        }

        val telecomManager = context.getSystemService(TelecomManager::class.java) ?: return false

        return try {
            telecomManager.endCall()
        } catch (exception: SecurityException) {
            Log.w(TAG, "Unable to decline incoming call", exception)
            false
        } catch (exception: IllegalStateException) {
            Log.w(TAG, "Decline call failed due to invalid state", exception)
            false
        }
    }

    private fun disconnectCall(call: Call): Boolean {
        return try {
            call.disconnect()
            true
        } catch (exception: SecurityException) {
            Log.w(TAG, "Unable to disconnect active call", exception)
            false
        } catch (exception: IllegalStateException) {
            Log.w(TAG, "Disconnect call failed due to invalid state", exception)
            false
        }
    }

    private fun rejectCall(call: Call): Boolean {
        return try {
            call.reject(false, null)
            true
        } catch (exception: SecurityException) {
            Log.w(TAG, "Unable to reject ringing call", exception)
            false
        } catch (exception: IllegalStateException) {
            Log.w(TAG, "Reject call failed due to invalid state", exception)
            false
        }
    }

    private fun hasAnswerPermission(context: Context): Boolean {
        return ContextCompat.checkSelfPermission(
            context,
            Manifest.permission.ANSWER_PHONE_CALLS
        ) == PackageManager.PERMISSION_GRANTED
    }
}
