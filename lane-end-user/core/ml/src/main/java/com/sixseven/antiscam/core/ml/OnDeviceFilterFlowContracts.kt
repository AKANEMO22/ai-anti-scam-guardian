package com.sixseven.antiscam.core.ml

enum class OnDeviceFilterSignalType {
    SMS,
    CALL,
    URL,
}

data class BackgroundServiceSignalPayload(
    val signalType: OnDeviceFilterSignalType,
    val rawInput: String,
    val sessionId: String? = null,
    val metadata: Map<String, String> = emptyMap(),
)

data class BackgroundToOnDeviceFilterRequest(
    val payload: BackgroundServiceSignalPayload,
    val source: String = "background-service",
)

data class OnDeviceFilterPipelineResult(
    val suspicious: Boolean,
    val maskedPayload: String,
    val confidence: Float,
    val signalType: OnDeviceFilterSignalType,
    val metadata: Map<String, String> = emptyMap(),
)