package com.sixseven.antiscam.domain.usecase

import com.sixseven.antiscam.domain.model.SignalPayload
import com.sixseven.antiscam.domain.model.SourceType

class ClassifyCallAuthenticityUseCase(
    private val processSignalPipelineUseCase: ProcessSignalPipelineUseCase
) {
    suspend operator fun invoke(transcript: String, sessionId: String): Int {
        val payload = SignalPayload(
            sourceType = SourceType.CALL,
            rawText = transcript,
            callSessionId = sessionId
        )
        return processSignalPipelineUseCase(payload).total
    }
}
