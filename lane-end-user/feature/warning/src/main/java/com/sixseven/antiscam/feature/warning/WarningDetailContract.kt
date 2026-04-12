package com.sixseven.antiscam.feature.warning

data class WarningDetailUiState(
    val score: Int,
    val severity: String,
    val explanation: String,
    val actionButtons: List<String> = listOf("Block", "Report", "Ignore", "Notify Guardian"),
    val feedbackOptions: List<String> = listOf("Scam", "Safe", "Not sure"),
)
