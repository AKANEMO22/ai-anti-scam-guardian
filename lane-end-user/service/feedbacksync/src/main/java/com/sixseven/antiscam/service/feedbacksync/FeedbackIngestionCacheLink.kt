package com.sixseven.antiscam.service.feedbacksync

class FeedbackIngestionCacheLink {
    fun forwardFeedbackIngestionToCacheLayer(
        request: FeedbackIngestionToCacheRequest,
    ): FeedbackCacheAck {
        // TODO: forward feedback ingestion result to Redis cache layer.
        throw NotImplementedError("Stub only")
    }

    fun buildFeedbackRedisKeyForPhoneUrlScript(
        payload: FeedbackLabelPayload,
    ): String {
        // TODO: build redis cache key for phone/url/script feedback channels.
        throw NotImplementedError("Stub only")
    }

    fun traceFeedbackIngestionToCacheFlow(
        request: FeedbackIngestionToCacheRequest,
    ) {
        // TODO: emit trace for feedback ingestion -> cache-layer flow.
    }
}