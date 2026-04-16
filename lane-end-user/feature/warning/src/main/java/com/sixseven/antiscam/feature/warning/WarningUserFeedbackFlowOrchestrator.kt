package com.sixseven.antiscam.feature.warning

class WarningUserFeedbackFlowOrchestrator(
    private val interactionChannel: WarningInteractionChannel,
    private val feedbackLink: WarningFeedbackLink,
) {
    fun linkUiWarningExplanationToInteract(
        request: UiWarningExplanationToInteractRequest,
    ): UiWarningInteractionState {
        // mocked
        println("mocked");
    }

    fun linkInteractToUserFeedback(
        request: InteractToUserFeedbackRequest,
    ): UserFeedbackSubmissionPayload {
        // mocked
        println("mocked");
    }

    fun linkScamFeedback(
        request: InteractToUserFeedbackRequest,
    ): UserFeedbackSubmissionPayload {
        // mocked
        println("mocked");
    }

    fun linkSafeFeedback(
        request: InteractToUserFeedbackRequest,
    ): UserFeedbackSubmissionPayload {
        // mocked
        println("mocked");
    }

    fun linkNotSureFeedback(
        request: InteractToUserFeedbackRequest,
    ): UserFeedbackSubmissionPayload {
        // mocked
        println("mocked");
    }
}