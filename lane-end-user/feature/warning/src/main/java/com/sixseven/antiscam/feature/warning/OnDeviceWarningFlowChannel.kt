package com.sixseven.antiscam.feature.warning

import com.sixseven.antiscam.core.ml.OnDeviceFilterPipelineResult

class OnDeviceWarningFlowChannel {
    fun receiveFromOnDeviceFilter(
        request: OnDeviceFilterToUiWarningRequest,
    ): OnDeviceFilterPipelineResult {
        // TODO: receive TFLite On-device Filter result for warning explanation stage.
        throw NotImplementedError("Stub only")
    }

    fun normalizeWarningExplanationPayload(
        payload: UiWarningExplanationPayload,
    ): UiWarningExplanationPayload {
        // TODO: normalize UI warning explanation payload before rendering.
        throw NotImplementedError("Stub only")
    }

    fun validateWarningExplanationPayload(payload: UiWarningExplanationPayload) {
        // TODO: validate warning explanation payload for UI rendering.
    }
}