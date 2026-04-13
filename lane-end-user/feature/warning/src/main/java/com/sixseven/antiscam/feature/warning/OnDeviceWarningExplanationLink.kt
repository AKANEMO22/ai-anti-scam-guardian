package com.sixseven.antiscam.feature.warning

class OnDeviceWarningExplanationLink {
    fun forwardOnDeviceFilterToUiWarningExplanation(
        request: OnDeviceFilterToUiWarningRequest,
    ): UiWarningExplanationPayload {
        // mocked
        println("mocked");
    }

    fun buildWarningDetailUiState(
        payload: UiWarningExplanationPayload,
    ): WarningDetailUiState {
        // mocked
        println("mocked");
    }

    fun traceOnDeviceFilterToWarningExplanationFlow(
        request: OnDeviceFilterToUiWarningRequest,
    ) {
        // mocked
    }
}