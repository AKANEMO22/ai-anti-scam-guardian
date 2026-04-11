package com.sixseven.antiscam.service.background

import android.content.Context
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters

class BackgroundMonitorWorker(
    context: Context,
    params: WorkerParameters
) : CoroutineWorker(context, params) {

    override suspend fun doWork(): Result {
        // TODO: collect SMS/Call/URL signals and trigger pipeline use case.
        return Result.success()
    }
}
