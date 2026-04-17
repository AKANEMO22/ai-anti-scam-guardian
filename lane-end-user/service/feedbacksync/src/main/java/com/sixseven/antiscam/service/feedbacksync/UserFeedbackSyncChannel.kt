package com.sixseven.antiscam.service.feedbacksync

class UserFeedbackSyncChannel {
    fun receiveFromWarningInteraction(
        request: UserFeedbackToSyncRequest,
    ): FeedbackSyncSubmissionPayload {
        // TODO: receive user feedback payload from warning interaction flow.
        throw NotImplementedError("Stub only")
    }

    fun normalizeFeedbackSyncPayload(
        payload: FeedbackSyncSubmissionPayload,
    ): FeedbackSyncSubmissionPayload {
        // TODO: normalize scam/safe/not sure payload before sync submission.
        throw NotImplementedError("Stub only")
    }

    fun validateFeedbackSyncPayload(payload: FeedbackSyncSubmissionPayload) {
        // TODO: validate feedback payload for ingestion endpoint contract.
    }
}