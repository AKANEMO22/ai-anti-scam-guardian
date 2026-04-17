package com.sixseven.antiscam.service.feedbacksync

import android.content.Context
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters

class FeedbackSyncWorker(
    context: Context,
    params: WorkerParameters
) : CoroutineWorker(context, params) {

    fun ingestUserFeedback(request: UserFeedbackToSyncRequest): FeedbackSyncAck {
        // TODO: entrypoint for warning interaction -> user feedback sync request.
        throw NotImplementedError("Stub only")
    }

    fun enqueueScamFeedback(payload: FeedbackSyncSubmissionPayload) {
        // TODO: enqueue scam feedback branch for sync.
    }

    fun enqueueSafeFeedback(payload: FeedbackSyncSubmissionPayload) {
        // TODO: enqueue safe feedback branch for sync.
    }

    fun enqueueNotSureFeedback(payload: FeedbackSyncSubmissionPayload) {
        // TODO: enqueue not-sure feedback branch for sync.
    }

    fun dispatchFeedbackToIngestion(payload: FeedbackSyncSubmissionPayload) {
        // TODO: dispatch feedback payload to ingestion endpoint.
    }

    fun mapUserFeedbackToFeedbackLabel(
        request: UserFeedbackToFeedbackLabelRequest,
    ): FeedbackLabelPayload {
        // TODO: map user feedback into feedback-label stage payload.
        throw NotImplementedError("Stub only")
    }

    fun dispatchFeedbackLabelToIngestion(
        request: FeedbackLabelToIngestionRequest,
    ) {
        // TODO: dispatch feedback-label payload to ingestion stage.
    }

    fun dispatchFeedbackIngestionToCacheLayer(
        request: FeedbackIngestionToCacheRequest,
    ): FeedbackCacheAck {
        // TODO: dispatch feedback-ingestion result to cache layer (phone/url/script).
        throw NotImplementedError("Stub only")
    }

    override suspend fun doWork(): Result {
        // TODO: process feedback label -> feedback ingestion -> cache-layer flow.
        return Result.success()
    }
}
