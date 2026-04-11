package com.sixseven.antiscam.feature.guardian

data class GuardianConfig(
    val enabled: Boolean,
    val phoneNumber: String,
    val criticalThreshold: Int = 80
)
