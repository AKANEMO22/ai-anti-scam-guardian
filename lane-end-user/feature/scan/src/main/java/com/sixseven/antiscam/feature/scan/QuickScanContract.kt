package com.sixseven.antiscam.feature.scan

data class QuickScanRequest(
    val input: String,
    val sourceType: String
)

data class QuickScanResult(
    val score: Int,
    val severity: String,
    val explanation: String,
    val recommendation: String
)
