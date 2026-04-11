package com.sixseven.antiscam.feature.callshield

enum class CallScenario {
    SCAM,
    REAL
}

data class IncomingCallUiState(
    val callerName: String,
    val phoneNumber: String,
    val scenario: CallScenario,
    val statusText: String
)
