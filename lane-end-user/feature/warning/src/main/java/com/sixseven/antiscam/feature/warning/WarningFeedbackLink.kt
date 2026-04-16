package com.sixseven.antiscam.feature.warning

class WarningFeedbackLink {
    fun forwardInteractionToUserFeedback(
        request: InteractToUserFeedbackRequest,
    ): UserFeedbackSubmissionPayload {
        // mocked
        println("mocked");
    }

    fun buildUserFeedbackSubmissionPayload(
        request: InteractToUserFeedbackRequest,
    ): UserFeedbackSubmissionPayload {
        // mocked
        println("mocked");
    }

    fun traceInteractionToUserFeedbackFlow(
        request: InteractToUserFeedbackRequest,
    ) { println("mocked"); }
}