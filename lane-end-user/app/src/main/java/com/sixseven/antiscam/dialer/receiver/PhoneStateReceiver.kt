package com.sixseven.antiscam.dialer.receiver

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.telephony.TelephonyManager
import com.sixseven.antiscam.dialer.call.ActiveCallStore
import com.sixseven.antiscam.dialer.call.FallbackRingingStore
import com.sixseven.antiscam.dialer.role.DefaultDialerRoleHelper
import com.sixseven.antiscam.dialer.ui.CallNotificationController

class PhoneStateReceiver : BroadcastReceiver() {

    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action != TelephonyManager.ACTION_PHONE_STATE_CHANGED) {
            return
        }

        if (!DefaultDialerRoleHelper.isDefaultDialer(context)) {
            return
        }

        runCatching {
            when (intent.getStringExtra(TelephonyManager.EXTRA_STATE)) {
                TelephonyManager.EXTRA_STATE_RINGING -> {
                    val incomingNumber = intent.getStringExtra(TelephonyManager.EXTRA_INCOMING_NUMBER)
                    FallbackRingingStore.onRinging(incomingNumber)
                    val hasTelecomCall = ActiveCallStore.current() != null
                    if (!hasTelecomCall && FallbackRingingStore.consumeLaunchRequest()) {
                        CallNotificationController.showIncomingCall(context, FallbackRingingStore.currentLabel())
                    }
                }

                TelephonyManager.EXTRA_STATE_OFFHOOK -> {
                    FallbackRingingStore.onCallEndedOrPicked()
                    CallNotificationController.cancel(context)
                }

                TelephonyManager.EXTRA_STATE_IDLE -> {
                    FallbackRingingStore.onCallEndedOrPicked()
                    ActiveCallStore.clear()
                    CallNotificationController.cancel(context)
                }
            }
        }
    }
}
