package com.sixseven.antiscam.domain.model

data class RiskScore(
    val total: Int,
    val voice: Int,
    val text: Int,
    val entity: Int,
    val explanation: String
) {
    val severity: Severity
        get() = when {
            total >= 80 -> Severity.HIGH
            total >= 55 -> Severity.MEDIUM
            else -> Severity.LOW
        }
}

enum class Severity {
    LOW, MEDIUM, HIGH
}
