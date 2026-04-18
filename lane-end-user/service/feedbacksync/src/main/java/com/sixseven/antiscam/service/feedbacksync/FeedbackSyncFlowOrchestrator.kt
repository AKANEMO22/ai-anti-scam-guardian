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
        // TODO: orchestrate warning feedback -> sync pipeline.
        throw NotImplementedError("Stub only")
    }

    fun linkScamFeedbackToSync(
        request: UserFeedbackToSyncRequest,
    ): FeedbackSyncAck {
        // TODO: orchestrate scam feedback sync branch.
        throw NotImplementedError("Stub only")
    }

    fun linkSafeFeedbackToSync(
        request: UserFeedbackToSyncRequest,
    ): FeedbackSyncAck {
        // TODO: orchestrate safe feedback sync branch.
        throw NotImplementedError("Stub only")
    }

    fun linkNotSureFeedbackToSync(
        request: UserFeedbackToSyncRequest,
    ): FeedbackSyncAck {
        // TODO: orchestrate not-sure feedback sync branch.
        throw NotImplementedError("Stub only")
    }

    fun linkUserFeedbackToFeedbackLabel(
        request: UserFeedbackToFeedbackLabelRequest,
    ): FeedbackLabelPayload {
        // TODO: orchestrate user feedback -> feedback-label stage.
        throw NotImplementedError("Stub only")
    }

    fun linkFeedbackLabelToFeedbackIngestion(
        request: FeedbackLabelToIngestionRequest,
    ): FeedbackSyncAck {
        // TODO: orchestrate feedback-label -> feedback-ingestion stage.
        throw NotImplementedError("Stub only")
    }

    fun linkFeedbackIngestionToCacheLayer(
        request: FeedbackIngestionToCacheRequest,
    ): FeedbackCacheAck {
        // TODO: orchestrate feedback-ingestion -> cache-layer stage for phone/url/script.
        throw NotImplementedError("Stub only")
    }

    fun linkScamFeedbackIngestionToCache(
        request: FeedbackIngestionToCacheRequest,
    ): FeedbackCacheAck {
        // TODO: orchestrate scam feedback branch to cache layer.
        throw NotImplementedError("Stub only")
    }

    fun linkSafeFeedbackIngestionToCache(
        request: FeedbackIngestionToCacheRequest,
    ): FeedbackCacheAck {
        // TODO: orchestrate safe feedback branch to cache layer.
        throw NotImplementedError("Stub only")
    }

    fun linkNotSureFeedbackIngestionToCache(
        request: FeedbackIngestionToCacheRequest,
    ): FeedbackCacheAck {
        // TODO: orchestrate not-sure feedback branch to cache layer.
        throw NotImplementedError("Stub only")
    }
}