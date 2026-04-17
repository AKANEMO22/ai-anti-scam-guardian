package com.sixseven.antiscam.incoming

object IncomingCallContracts {
    const val CHANNEL_ID = "incoming_call_ui_v2"
    const val CHANNEL_NAME = "Incoming Call Alerts"
    const val NOTIFICATION_ID = 4401

    const val ACTION_ANSWER = "com.sixseven.antiscam.action.ANSWER_CALL"
    const val ACTION_DECLINE = "com.sixseven.antiscam.action.DECLINE_CALL"
    const val ACTION_CALL_STATE_CHANGED = "com.sixseven.antiscam.action.CALL_STATE_CHANGED"

    const val EXTRA_CALLER_LABEL = "extra_caller_label"
    const val EXTRA_CALL_STATE = "extra_call_state"

    const val STATE_ANSWER_FAILED = "ANSWER_FAILED"
    const val STATE_DECLINE_FAILED = "DECLINE_FAILED"
}
