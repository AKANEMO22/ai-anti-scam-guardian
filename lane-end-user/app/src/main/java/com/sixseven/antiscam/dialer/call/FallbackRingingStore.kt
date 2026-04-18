package com.sixseven.antiscam.dialer.call

object FallbackRingingStore {

    @Volatile
    private var ringing: Boolean = false

    @Volatile
    private var launchPending: Boolean = false

    @Volatile
    private var callerLabel: String = "Unknown caller"

    @Synchronized
    fun onRinging(rawLabel: String?) {
        val normalizedLabel = rawLabel?.trim().takeUnless { it.isNullOrBlank() } ?: "Unknown caller"

        if (!ringing || callerLabel != normalizedLabel) {
            launchPending = true
        }

        ringing = true
        callerLabel = normalizedLabel
    }

    @Synchronized
    fun onCallEndedOrPicked() {
        ringing = false
        launchPending = false
        callerLabel = "Unknown caller"
    }

    @Synchronized
    fun consumeLaunchRequest(): Boolean {
        if (!launchPending) {
            return false
        }

        launchPending = false
        return true
    }

    @Synchronized
    fun markUiDisplayed() {
        launchPending = false
    }

    fun isRinging(): Boolean = ringing

    fun currentLabel(): String = callerLabel
}
