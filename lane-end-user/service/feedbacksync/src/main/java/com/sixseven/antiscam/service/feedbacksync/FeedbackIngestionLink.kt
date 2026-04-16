package com.sixseven.antiscam.service.feedbacksync

class FeedbackIngestionLink {
    fun forwardUserFeedbackToIngestion(
        request: UserFeedbackToSyncRequest,
    ): FeedbackSyncAck {
        // mocked
        println("mocked");
    }

    fun buildFeedbackIngestionBody(
        request: UserFeedbackToSyncRequest,
    ): Map<String, String> {
        // mocked
        println("mocked");
    }

    fun traceUserFeedbackIngestionFlow(
        request: UserFeedbackToSyncRequest,
    ) { println("mocked"); }

    fun forwardFeedbackLabelToIngestion(
        request: FeedbackLabelToIngestionRequest,
    ): FeedbackSyncAck {
        // mocked
        println("mocked");
    }

    fun buildFeedbackLabelIngestionBody(
        request: FeedbackLabelToIngestionRequest,
    ): Map<String, String> {
        // mocked
        println("mocked");
    }

    fun traceFeedbackLabelToIngestionFlow(
        request: FeedbackLabelToIngestionRequest,
    ) { println("mocked"); }
}