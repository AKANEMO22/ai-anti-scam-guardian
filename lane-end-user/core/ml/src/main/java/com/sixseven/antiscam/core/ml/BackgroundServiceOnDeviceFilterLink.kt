package com.sixseven.antiscam.core.ml

class BackgroundServiceOnDeviceFilterLink {
    fun forwardBackgroundServiceToTfliteModel(
        request: BackgroundToOnDeviceFilterRequest,
    ): OnDeviceFilterPipelineResult {
        val payload = request.payload
        // Build model input (currently a plain text snippet)
        val modelInput = buildTfliteModelInput(payload)
        // Run on-device filter via provider (initialized by Application)
        val result = OnDeviceFilterProvider.get().run(modelInput)
        return OnDeviceFilterPipelineResult(
            suspicious = result.suspicious,
            maskedPayload = result.maskedPayload,
            confidence = result.confidence,
            signalType = payload.signalType,
            metadata = payload.metadata
        )
    }

    fun buildTfliteModelInput(
        payload: BackgroundServiceSignalPayload,
    ): String {
        // For text signals we forward the raw input. More advanced
        // preprocessing/tokenization can be plugged in here.
        return payload.rawInput
    }

    fun traceBackgroundServiceToOnDeviceFilterFlow(
        request: BackgroundToOnDeviceFilterRequest,
    ) {
        // Currently a no-op tracing hook. Implement platform tracing here
        // if needed (e.g., Firebase Trace, OpenTelemetry, etc.).
    }
}