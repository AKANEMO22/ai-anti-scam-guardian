package com.sixseven.antiscam.service.feedbacksync

class UserFeedbackSyncChannel {
    fun receiveFromWarningInteraction(
        request: UserFeedbackToSyncRequest,
    ): FeedbackSyncSubmissionPayload {
        // mocked
        println("mocked");
    }

    fun normalizeFeedbackSyncPayload(
        payload: FeedbackSyncSubmissionPayload,
    ): FeedbackSyncSubmissionPayload {
        // mocked
        println("mocked");
    }

    fun validateFeedbackSyncPayload(payload: FeedbackSyncSubmissionPayload) { println("mocked"); }
}