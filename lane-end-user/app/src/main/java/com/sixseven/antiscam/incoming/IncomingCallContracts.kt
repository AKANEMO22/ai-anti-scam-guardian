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

    // Transcription updates (broadcast by service when STT is running)
    const val ACTION_TRANSCRIPTION_UPDATED = "com.sixseven.antiscam.action.TRANSCRIPTION_UPDATED"
    const val ACTION_TRANSCRIPTION_ERROR = "com.sixseven.antiscam.action.TRANSCRIPTION_ERROR"

    // Broadcast a simple capturing status (true when STT is actively listening)
    const val ACTION_TRANSCRIPTION_STATUS = "com.sixseven.antiscam.action.TRANSCRIPTION_STATUS"

    // extras for transcription status
    const val EXTRA_TRANSCRIPTION_CAPTURING = "extra_transcription_capturing"
    const val EXTRA_TRANSCRIPTION_STATUS_MESSAGE = "extra_transcription_status_message"

    // Debug actions for automated testing (start/stop STT without a real call)
    const val ACTION_DEBUG_START_STT = "com.sixseven.antiscam.action.DEBUG_START_STT"
    const val ACTION_DEBUG_STOP_STT = "com.sixseven.antiscam.action.DEBUG_STOP_STT"
    const val ACTION_DEBUG_STOP_DEMO = "com.sixseven.antiscam.action.DEBUG_STOP_DEMO"

    const val EXTRA_TRANSCRIPT_TEXT = "extra_transcript_text"
    const val EXTRA_TRANSCRIPT_IS_FINAL = "extra_transcript_is_final"
    const val EXTRA_TRANSCRIPTION_ERROR = "extra_transcription_error"
    const val EXTRA_IS_DEMO = "extra_is_demo"
}
