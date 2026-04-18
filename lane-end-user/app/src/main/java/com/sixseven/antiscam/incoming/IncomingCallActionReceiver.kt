package com.sixseven.antiscam.incoming

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.telephony.TelephonyManager

class IncomingCallActionReceiver : BroadcastReceiver() {

    override fun onReceive(context: Context, intent: Intent?) {
        val callerLabel = intent?.getStringExtra(IncomingCallContracts.EXTRA_CALLER_LABEL)

        when (intent?.action) {
            IncomingCallContracts.ACTION_ANSWER -> {
                val answered = IncomingCallControl.answer(context)
                if (answered) {
                    launchCallUi(context, callerLabel, TelephonyManager.EXTRA_STATE_OFFHOOK)
                    broadcastCallState(context, TelephonyManager.EXTRA_STATE_OFFHOOK, callerLabel)
                    return
                }

                launchCallUi(context, callerLabel, IncomingCallContracts.STATE_ANSWER_FAILED)
                broadcastCallState(context, IncomingCallContracts.STATE_ANSWER_FAILED, callerLabel)
            }

            IncomingCallContracts.ACTION_DECLINE -> {
                val declined = IncomingCallControl.decline(context)
                IncomingCallStateStore.clear()
                IncomingCallNotifier.cancelIncomingCall(context)

                if (declined) {
                    launchCallUi(context, callerLabel, TelephonyManager.EXTRA_STATE_IDLE)
                    broadcastCallState(context, TelephonyManager.EXTRA_STATE_IDLE, callerLabel)
                    return
                }

                launchCallUi(context, callerLabel, IncomingCallContracts.STATE_DECLINE_FAILED)
                broadcastCallState(context, IncomingCallContracts.STATE_DECLINE_FAILED, callerLabel)
            }
        }
    }

    private fun launchCallUi(context: Context, callerLabel: String?, state: String) {
        val callUiIntent = Intent(context, IncomingCallActivity::class.java).apply {
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP)
            addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP)
            putExtra(IncomingCallContracts.EXTRA_CALLER_LABEL, callerLabel)
            putExtra(IncomingCallContracts.EXTRA_CALL_STATE, state)
        }
        context.startActivity(callUiIntent)
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
