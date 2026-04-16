package com.sixseven.antiscam.incoming

object IncomingCallStateStore {
    private const val FALLBACK_LABEL = "Số đang gọi"

    private val lock = Any()
    private var ringing = false
    private var currentLabel = FALLBACK_LABEL

    fun onRinging(rawNumber: String?): Boolean {
        synchronized(lock) {
            val normalized = rawNumber?.trim().takeUnless { it.isNullOrBlank() } ?: FALLBACK_LABEL
            val shouldRefresh = !ringing || currentLabel != normalized
            ringing = true
            currentLabel = normalized
            return shouldRefresh
        }
    }

    fun clear() {
        synchronized(lock) {
            ringing = false
            currentLabel = FALLBACK_LABEL
        }
    }

    fun currentLabel(): String = synchronized(lock) { currentLabel }
}
