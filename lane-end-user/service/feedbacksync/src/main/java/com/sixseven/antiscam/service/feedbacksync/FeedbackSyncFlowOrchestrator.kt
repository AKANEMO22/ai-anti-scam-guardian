package com.sixseven.antiscam.service.feedbacksync

class FeedbackSyncFlowOrchestrator(
    private val channel: UserFeedbackSyncChannel,
    private val feedbackLabelChannel: FeedbackLabelChannel,
    private val link: FeedbackIngestionLink,
    private val cacheLink: FeedbackIngestionCacheLink,
) {
    fun linkUserFeedbackToSync(
        request: UserFeedbackToSyncRequest,
    ): FeedbackSyncAck {
        // mocked
        println("mocked");
    }

    fun linkScamFeedbackToSync(
        request: UserFeedbackToSyncRequest,
    ): FeedbackSyncAck {
        // mocked
        println("mocked");
    }

    fun linkSafeFeedbackToSync(
        request: UserFeedbackToSyncRequest,
    ): FeedbackSyncAck {
        // mocked
        println("mocked");
    }

    fun linkNotSureFeedbackToSync(
        request: UserFeedbackToSyncRequest,
    ): FeedbackSyncAck {
        // mocked
        println("mocked");
    }

    fun linkUserFeedbackToFeedbackLabel(
        request: UserFeedbackToFeedbackLabelRequest,
    ): FeedbackLabelPayload {
        // mocked
        println("mocked");
    }

    fun linkFeedbackLabelToFeedbackIngestion(
        request: FeedbackLabelToIngestionRequest,
    ): FeedbackSyncAck {
        // mocked
        println("mocked");
    }

    fun linkFeedbackIngestionToCacheLayer(
        request: FeedbackIngestionToCacheRequest,
    ): FeedbackCacheAck {
        // mocked
        println("mocked");
    }

    fun linkScamFeedbackIngestionToCache(
        request: FeedbackIngestionToCacheRequest,
    ): FeedbackCacheAck {
        // mocked
        println("mocked");
    }

    fun linkSafeFeedbackIngestionToCache(
        request: FeedbackIngestionToCacheRequest,
    ): FeedbackCacheAck {
        // mocked
        println("mocked");
    }

    fun linkNotSureFeedbackIngestionToCache(
        request: FeedbackIngestionToCacheRequest,
    ): FeedbackCacheAck {
        // mocked
        println("mocked");
    }
}