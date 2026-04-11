package com.sixseven.antiscam.data.remote

import com.sixseven.antiscam.core.network.CloudApi
import com.sixseven.antiscam.core.network.RiskResponse
import com.sixseven.antiscam.core.network.SignalRequest

class CloudRunApiDataSource(
    private val cloudApi: CloudApi
) {
    suspend fun analyze(request: SignalRequest): RiskResponse = cloudApi.analyzeSignal(request)

    suspend fun pushFeedback(eventId: String, label: String): Boolean =
        cloudApi.submitFeedback(eventId, label)
}
