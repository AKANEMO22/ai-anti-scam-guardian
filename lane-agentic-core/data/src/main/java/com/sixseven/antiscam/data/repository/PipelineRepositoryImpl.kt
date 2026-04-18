package com.sixseven.antiscam.data.repository

import com.sixseven.antiscam.core.ml.OnDeviceFilter
import com.sixseven.antiscam.core.network.SignalRequest
import com.sixseven.antiscam.data.local.RiskEvent
import com.sixseven.antiscam.data.local.RiskEventLocalStore
import com.sixseven.antiscam.data.remote.CloudRunApiDataSource
import com.sixseven.antiscam.domain.model.RiskScore
import com.sixseven.antiscam.domain.model.SignalPayload
import com.sixseven.antiscam.domain.usecase.PipelineRepository
import java.util.UUID

class PipelineRepositoryImpl(
    private val onDeviceFilter: OnDeviceFilter,
    private val cloudRunApiDataSource: CloudRunApiDataSource,
    private val localStore: RiskEventLocalStore
) : PipelineRepository {

    override suspend fun processSignal(payload: SignalPayload): RiskScore {
        val local = onDeviceFilter.run(payload.rawText)
        val response = cloudRunApiDataSource.analyze(
            SignalRequest(
                sourceType = payload.sourceType.name,
                text = local.maskedPayload,
                callSessionId = payload.callSessionId,
                metadata = payload.metadata
            )
        )

        val risk = RiskScore(
            total = response.riskScore,
            voice = response.voiceScore,
            text = response.textScore,
            entity = response.entityScore,
            explanation = response.explanation
        )

        localStore.insert(
            RiskEvent(
                eventId = UUID.randomUUID().toString(),
                sourceType = payload.sourceType.name,
                riskScore = risk.total,
                explanation = risk.explanation,
                createdAt = System.currentTimeMillis()
            )
        )

        return risk
    }

    override suspend fun submitFeedback(eventId: String, label: String): Boolean {
        return cloudRunApiDataSource.pushFeedback(eventId, label)
    }
}
