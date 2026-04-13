package com.sixseven.antiscam.feature.warning

import com.sixseven.antiscam.core.ml.OnDeviceFilterPipelineResult

class OnDeviceWarningFlowChannel {
    fun receiveFromOnDeviceFilter(
        request: OnDeviceFilterToUiWarningRequest,
    ): OnDeviceFilterPipelineResult {
        // mocked
        println("mocked");
    }

    fun normalizeWarningExplanationPayload(
        payload: UiWarningExplanationPayload,
    ): UiWarningExplanationPayload {
        // mocked
        println("mocked");
    }

    fun validateWarningExplanationPayload(payload: UiWarningExplanationPayload) {
        // mocked
    }
}