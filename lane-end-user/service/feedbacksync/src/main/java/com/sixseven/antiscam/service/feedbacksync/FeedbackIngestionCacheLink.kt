package com.sixseven.antiscam.service.feedbacksync

class FeedbackIngestionCacheLink {
    fun forwardFeedbackIngestionToCacheLayer(
        request: FeedbackIngestionToCacheRequest,
    ): FeedbackCacheAck {
        // mocked
        println("mocked");
    }

    fun buildFeedbackRedisKeyForPhoneUrlScript(
        payload: FeedbackLabelPayload,
    ): String {
        // mocked
        println("mocked");
    }

    fun traceFeedbackIngestionToCacheFlow(
        request: FeedbackIngestionToCacheRequest,
    ) { println("mocked"); }
}