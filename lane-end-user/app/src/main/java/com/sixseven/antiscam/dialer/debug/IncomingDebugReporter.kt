package com.sixseven.antiscam.dialer.debug

import android.util.Log

object IncomingDebugReporter {
    private const val TAG = "IncomingDebug"

    fun report(event: String, details: Map<String, Any?> = emptyMap()) {
        if (details.isEmpty()) {
            Log.d(TAG, event)
            return
        }

        val serializedDetails = details.entries.joinToString(", ") { (key, value) -> "$key=$value" }
        Log.d(TAG, "$event | $serializedDetails")
    }
}
