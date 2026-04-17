package com.sixseven.antiscam.incoming

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.telephony.TelephonyManager

class IncomingCallReceiver : BroadcastReceiver() {

    override fun onReceive(context: Context, intent: Intent?) {
        if (intent?.action != TelephonyManager.ACTION_PHONE_STATE_CHANGED) {
            return
        }

        val state = intent.getStringExtra(TelephonyManager.EXTRA_STATE) ?: return

        when (state) {
            TelephonyManager.EXTRA_STATE_RINGING -> {
                val number = intent.getStringExtra(TelephonyManager.EXTRA_INCOMING_NUMBER)
                val shouldShowUi = IncomingCallStateStore.onRinging(number)
                val callerLabel = IncomingCallStateStore.currentLabel()

                if (shouldShowUi) {
                    IncomingCallNotifier.showIncomingCall(context, callerLabel)
                }

                broadcastCallState(context, state, callerLabel)
            }

            TelephonyManager.EXTRA_STATE_OFFHOOK,
            TelephonyManager.EXTRA_STATE_IDLE -> {
                IncomingCallNotifier.cancelIncomingCall(context)
                IncomingCallStateStore.clear()
                broadcastCallState(context, state, null)
            }
        }
    }

    private fun broadcastCallState(context: Context, state: String, callerLabel: String?) {
        context.sendBroadcast(
            Intent(IncomingCallContracts.ACTION_CALL_STATE_CHANGED).apply {
                setPackage(context.packageName)
                putExtra(IncomingCallContracts.EXTRA_CALL_STATE, state)
                putExtra(IncomingCallContracts.EXTRA_CALLER_LABEL, callerLabel)
            }
        )
    }
}
