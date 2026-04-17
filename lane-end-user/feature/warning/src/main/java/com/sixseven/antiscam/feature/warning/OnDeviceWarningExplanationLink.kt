package com.sixseven.antiscam.feature.warning

class OnDeviceWarningExplanationLink {
    fun forwardOnDeviceFilterToUiWarningExplanation(
        request: OnDeviceFilterToUiWarningRequest,
    ): UiWarningExplanationPayload {
        // TODO: forward TFLite output to warning explanation builder stage.
        throw NotImplementedError("Stub only")
    }

    fun buildWarningDetailUiState(
        payload: UiWarningExplanationPayload,
    ): WarningDetailUiState {
        // TODO: map explanation payload into warning detail UI state.
        throw NotImplementedError("Stub only")
    }

    fun traceOnDeviceFilterToWarningExplanationFlow(
        request: OnDeviceFilterToUiWarningRequest,
    ) {
        // TODO: emit trace event for TFLite -> UI warning explanation flow.
    }
}