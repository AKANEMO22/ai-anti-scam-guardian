package com.sixseven.antiscam.service.feedbacksync

class FeedbackLabelChannel {
    fun receiveFromUserFeedback(
        request: UserFeedbackToFeedbackLabelRequest,
    ): FeedbackLabelPayload {
        // mocked
        println("mocked");
    }

    fun normalizeFeedbackLabelPayload(
        payload: FeedbackLabelPayload,
    ): FeedbackLabelPayload {
        // mocked
        println("mocked");
    }

    fun validateFeedbackLabelPayload(payload: FeedbackLabelPayload) {
        // mocked
    }
}