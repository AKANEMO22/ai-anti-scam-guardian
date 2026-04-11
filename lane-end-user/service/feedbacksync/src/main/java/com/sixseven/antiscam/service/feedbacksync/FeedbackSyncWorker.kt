package com.sixseven.antiscam.service.feedbacksync

import android.content.Context
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters

class FeedbackSyncWorker(
    context: Context,
    params: WorkerParameters
) : CoroutineWorker(context, params) {

    override suspend fun doWork(): Result {
        // TODO: push Scam/Safe/Not sure labels to feedback ingestion endpoint.
        return Result.success()
    }
}
