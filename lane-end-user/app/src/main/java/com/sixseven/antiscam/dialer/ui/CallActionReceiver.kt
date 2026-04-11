package com.sixseven.antiscam.dialer.ui

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import com.sixseven.antiscam.dialer.call.CallControlFacade
import com.sixseven.antiscam.dialer.call.CallUiAction

class CallActionReceiver : BroadcastReceiver() {

    override fun onReceive(context: Context, intent: Intent) {
        runCatching {
            when (intent.action) {
                CallUiAction.ACTION_ANSWER -> {
                    val answered = CallControlFacade.answer(context)
                    if (answered) {
                        context.startActivity(InCallOngoingActivity.buildIntent(context))
                    } else {
                        context.startActivity(IncomingCallActivity.buildIntent(context))
                    }
                }

                CallUiAction.ACTION_DECLINE -> {
                    CallControlFacade.decline(context)
                }
            }

            CallNotificationController.cancel(context)
        }
    }
}
