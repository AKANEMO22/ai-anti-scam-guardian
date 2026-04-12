package com.sixseven.antiscam.service.feedbacksync

class FeedbackIngestionLink {
    fun forwardUserFeedbackToIngestion(
        request: UserFeedbackToSyncRequest,
    ): FeedbackSyncAck {
        // TODO: forward user feedback payload to ingestion transport stage.
        throw NotImplementedError("Stub only")
    }

    fun buildFeedbackIngestionBody(
        request: UserFeedbackToSyncRequest,
    ): Map<String, String> {
        // TODO: build request body for scam/safe/not sure feedback endpoint.
        throw NotImplementedError("Stub only")
    }

    fun traceUserFeedbackIngestionFlow(
        request: UserFeedbackToSyncRequest,
    ) {
        // TODO: emit trace for user feedback submission flow.
    }

    fun forwardFeedbackLabelToIngestion(
        request: FeedbackLabelToIngestionRequest,
    ): FeedbackSyncAck {
        // TODO: forward feedback-label payload to ingestion transport stage.
        throw NotImplementedError("Stub only")
    }

    fun buildFeedbackLabelIngestionBody(
        request: FeedbackLabelToIngestionRequest,
    ): Map<String, String> {
        // TODO: build ingestion body from feedback-label payload.
        throw NotImplementedError("Stub only")
    }

    fun traceFeedbackLabelToIngestionFlow(
        request: FeedbackLabelToIngestionRequest,
    ) {
        // TODO: emit trace for feedback-label -> feedback-ingestion flow.
    }
}