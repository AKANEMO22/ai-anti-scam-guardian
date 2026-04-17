package com.sixseven.antiscam.feature.warning

class WarningUserFeedbackFlowOrchestrator(
    private val interactionChannel: WarningInteractionChannel,
    private val feedbackLink: WarningFeedbackLink,
) {
    fun linkUiWarningExplanationToInteract(
        request: UiWarningExplanationToInteractRequest,
    ): UiWarningInteractionState {
        // TODO: orchestrate UI warning explanation -> interaction state.
        throw NotImplementedError("Stub only")
    }

    fun linkInteractToUserFeedback(
        request: InteractToUserFeedbackRequest,
    ): UserFeedbackSubmissionPayload {
        // TODO: orchestrate interaction state -> user feedback payload.
        throw NotImplementedError("Stub only")
    }

    fun linkScamFeedback(
        request: InteractToUserFeedbackRequest,
    ): UserFeedbackSubmissionPayload {
        // TODO: orchestrate scam feedback branch.
        throw NotImplementedError("Stub only")
    }

    fun linkSafeFeedback(
        request: InteractToUserFeedbackRequest,
    ): UserFeedbackSubmissionPayload {
        // TODO: orchestrate safe feedback branch.
        throw NotImplementedError("Stub only")
    }

    fun linkNotSureFeedback(
        request: InteractToUserFeedbackRequest,
    ): UserFeedbackSubmissionPayload {
        // TODO: orchestrate not-sure feedback branch.
        throw NotImplementedError("Stub only")
    }
}