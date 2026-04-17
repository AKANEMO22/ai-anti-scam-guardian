package com.sixseven.antiscam.core.network

data class SignalRequest(
    val sourceType: String,
    val text: String?,
    val callSessionId: String?,
    val metadata: Map<String, String> = emptyMap()
)

data class RiskResponse(
    val riskScore: Int,
    val explanation: String,
    val voiceScore: Int,
    val textScore: Int,
    val entityScore: Int,
    val cacheHit: Boolean
)

data class FeedbackRequest(
    val eventId: String,
    val userId: String,
    val label: String,
    val sourceType: String,
    val timestamp: String,
    val riskScore: Int? = null,
    val metadata: Map<String, String> = emptyMap()
)

data class FeedbackResponse(
    val accepted: Boolean
)

interface CloudApi {
    suspend fun analyzeSignal(request: SignalRequest): RiskResponse
    suspend fun submitFeedback(request: FeedbackRequest): FeedbackResponse
}
