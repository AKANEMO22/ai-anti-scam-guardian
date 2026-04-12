package com.sixseven.antiscam.feature.warning

class WarningFeedbackLink {
    fun forwardInteractionToUserFeedback(
        request: InteractToUserFeedbackRequest,
    ): UserFeedbackSubmissionPayload {
        // TODO: forward selected feedback label to user feedback payload stage.
        throw NotImplementedError("Stub only")
    }

    fun buildUserFeedbackSubmissionPayload(
        request: InteractToUserFeedbackRequest,
    ): UserFeedbackSubmissionPayload {
        // TODO: build scam/safe/not sure payload from interaction request.
        throw NotImplementedError("Stub only")
    }

    fun traceInteractionToUserFeedbackFlow(
        request: InteractToUserFeedbackRequest,
    ) {
        // TODO: emit trace for UI interaction -> user feedback flow.
    }
}