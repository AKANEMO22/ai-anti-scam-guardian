package com.sixseven.antiscam.feature.settings

data class ProtectionSettings(
    val monitorSmsCallUrl: Boolean = true,
    val piiMasking: Boolean = true,
    val realtimeCallShield: Boolean = true,
    val autoFeedbackSync: Boolean = false
)
