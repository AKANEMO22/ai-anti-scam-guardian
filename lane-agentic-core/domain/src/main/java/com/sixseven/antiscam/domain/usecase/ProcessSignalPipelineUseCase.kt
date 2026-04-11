package com.sixseven.antiscam.domain.usecase

import com.sixseven.antiscam.domain.model.RiskScore
import com.sixseven.antiscam.domain.model.SignalPayload

interface PipelineRepository {
    suspend fun processSignal(payload: SignalPayload): RiskScore
    suspend fun submitFeedback(eventId: String, label: String): Boolean
}

class ProcessSignalPipelineUseCase(
    private val repository: PipelineRepository
) {
    suspend operator fun invoke(payload: SignalPayload): RiskScore {
        return repository.processSignal(payload)
    }
}
