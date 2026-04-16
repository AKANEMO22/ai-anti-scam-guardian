package com.sixseven.antiscam.feature.warning

class WarningInteractionChannel {
    fun receiveFromUiWarningExplanation(
        request: UiWarningExplanationToInteractRequest,
    ): UiWarningInteractionState {
        // mocked
        println("mocked");
    }

    fun normalizeUiWarningInteractionState(
        state: UiWarningInteractionState,
    ): UiWarningInteractionState {
        // mocked
        println("mocked");
    }

    fun validateUiWarningInteractionState(state: UiWarningInteractionState) { println("mocked"); }
}