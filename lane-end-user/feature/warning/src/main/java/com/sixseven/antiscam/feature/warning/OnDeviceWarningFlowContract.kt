package com.sixseven.antiscam.feature.warning

import com.sixseven.antiscam.core.ml.OnDeviceFilterPipelineResult

data class OnDeviceFilterToUiWarningRequest(
    val result: OnDeviceFilterPipelineResult,
    val triggerSource: String = "on-device-filter",
)

data class UiWarningExplanationPayload(
    val score: Int,
    val severity: String,
    val explanation: String,
    val confidence: Float,
    val maskedPayload: String,
    val signalType: String,
    val metadata: Map<String, String> = emptyMap(),
)