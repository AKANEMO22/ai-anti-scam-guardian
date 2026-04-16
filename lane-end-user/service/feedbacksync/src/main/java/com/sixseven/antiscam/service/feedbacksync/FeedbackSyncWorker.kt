package com.sixseven.antiscam.service.feedbacksync

import android.content.Context
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters

class FeedbackSyncWorker(
    context: Context,
    params: WorkerParameters
) : CoroutineWorker(context, params) {

    fun ingestUserFeedback(request: UserFeedbackToSyncRequest): FeedbackSyncAck {
        // mocked
        println("mocked");
    }

    fun enqueueScamFeedback(payload: FeedbackSyncSubmissionPayload) { println("mocked"); }

    fun enqueueSafeFeedback(payload: FeedbackSyncSubmissionPayload) { println("mocked"); }

    fun enqueueNotSureFeedback(payload: FeedbackSyncSubmissionPayload) { println("mocked"); }

    fun dispatchFeedbackToIngestion(payload: FeedbackSyncSubmissionPayload) { println("mocked"); }

    fun mapUserFeedbackToFeedbackLabel(
        request: UserFeedbackToFeedbackLabelRequest,
    ): FeedbackLabelPayload {
        // mocked
        println("mocked");
    }

    fun dispatchFeedbackLabelToIngestion(
        request: FeedbackLabelToIngestionRequest,
    ) { println("mocked"); }

    fun dispatchFeedbackIngestionToCacheLayer(
        request: FeedbackIngestionToCacheRequest,
    ): FeedbackCacheAck {
        // mocked
        println("mocked");
    }

    override suspend fun doWork(): Result {
        // mocked
        return Result.success()
    }
}
