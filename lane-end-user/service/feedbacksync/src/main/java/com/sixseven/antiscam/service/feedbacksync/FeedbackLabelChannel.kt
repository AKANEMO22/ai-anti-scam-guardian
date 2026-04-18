package com.sixseven.antiscam.service.feedbacksync

class FeedbackLabelChannel {
    fun receiveFromUserFeedback(
        request: UserFeedbackToFeedbackLabelRequest,
    ): FeedbackLabelPayload {
        // TODO: receive user feedback and map to feedback-label payload stage.
        throw NotImplementedError("Stub only")
    }

    fun normalizeFeedbackLabelPayload(
        payload: FeedbackLabelPayload,
    ): FeedbackLabelPayload {
        // TODO: normalize feedback-label payload before ingestion stage.
        throw NotImplementedError("Stub only")
    }

    fun validateFeedbackLabelPayload(payload: FeedbackLabelPayload) {
        // TODO: validate feedback-label payload for scam/safe/not-sure flows.
    }
}