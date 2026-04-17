package com.sixseven.antiscam.domain.model

data class SignalPayload(
    val sourceType: SourceType,
    val rawText: String,
    val callSessionId: String? = null,
    val metadata: Map<String, String> = emptyMap()
)

enum class SourceType {
    SMS,
    URL,
    CALL
}
