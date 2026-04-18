package com.sixseven.antiscam.data.remote

import com.sixseven.antiscam.core.network.CloudApi
import com.sixseven.antiscam.core.network.RiskResponse
import com.sixseven.antiscam.core.network.SignalRequest
import com.sixseven.antiscam.core.network.FeedbackRequest

class CloudRunApiDataSource(
    private val cloudApi: CloudApi
) {
    suspend fun analyze(request: SignalRequest): RiskResponse = cloudApi.analyzeSignal(request)

    suspend fun pushFeedback(eventId: String, label: String): Boolean {
        val req = FeedbackRequest(
            eventId = eventId,
            userId = "mobile",
            label = label,
            sourceType = "SMS",
            timestamp = java.time.Instant.now().toString(),
            riskScore = null,
            metadata = emptyMap()
        )

        val resp = cloudApi.submitFeedback(req)
        return resp.accepted
    }
}
