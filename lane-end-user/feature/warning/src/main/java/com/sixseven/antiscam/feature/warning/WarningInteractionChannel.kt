package com.sixseven.antiscam.feature.warning

class WarningInteractionChannel {
    fun receiveFromUiWarningExplanation(
        request: UiWarningExplanationToInteractRequest,
    ): UiWarningInteractionState {
        // TODO: receive warning explanation and prepare interaction state.
        throw NotImplementedError("Stub only")
    }

    fun normalizeUiWarningInteractionState(
        state: UiWarningInteractionState,
    ): UiWarningInteractionState {
        // TODO: normalize interaction state before user feedback selection.
        throw NotImplementedError("Stub only")
    }

    fun validateUiWarningInteractionState(state: UiWarningInteractionState) {
        // TODO: validate interaction state for feedback selection actions.
    }
}