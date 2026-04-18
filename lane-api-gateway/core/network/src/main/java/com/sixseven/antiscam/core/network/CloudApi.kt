package com.sixseven.antiscam.core.network

enum class SourceType {
    SMS, URL, CALL
}

enum class FeedbackLabel {
    SCAM, SAFE, NOT_SURE
}

data class SignalRequest(
    val sourceType: SourceType,
    val text: String? = null,
    val callSessionId: String? = null,
    val metadata: Map<String, String> = emptyMap()
)

data class MatchedPattern(
    val pattern_id: String,
    val pattern_text: String
)

data class RiskResponse(
    val riskScore: Int,
    val explanation: String,
    val voiceScore: Int = 0,
    val textScore: Int = 0,
    val entityScore: Int = 0,
    val piiScore: Int = 0,
    val engagementScore: Int = 0,
    val piiTypes: List<String> = emptyList(),
    val baiterResponse: String? = null,
    val cacheHit: Boolean = false,
    val matchedPatterns: List<MatchedPattern> = emptyList()
)

data class FeedbackEvent(
    val eventId: String,
    val userId: String,
    val label: FeedbackLabel,
    val sourceType: SourceType,
    val timestamp: String,
    val riskScore: Int? = null,
    val metadata: Map<String, String> = emptyMap()
)

data class FeedbackResponse(
    val accepted: Boolean
)

interface CloudApi {
    suspend fun analyzeSignal(request: SignalRequest): RiskResponse
    suspend fun submitFeedback(request: FeedbackEvent): FeedbackResponse
}
