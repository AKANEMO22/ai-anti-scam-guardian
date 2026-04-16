package com.sixseven.antiscam.service.background

import android.content.Context
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.sixseven.antiscam.core.ml.OnDeviceFilterPipelineResult

class BackgroundMonitorWorker(
    context: Context,
    params: WorkerParameters
) : CoroutineWorker(context, params) {

    fun ingestMobileAppSignal(request: MobileAppToBackgroundServiceRequest): BackgroundServiceDispatchAck {
        // mocked
        println("mocked");
    }

    fun collectSmsSignalsFromMobileApp(payload: MobileBackgroundSignalPayload) { println("mocked"); }

    fun collectCallSignalsFromMobileApp(payload: MobileBackgroundSignalPayload) { println("mocked"); }

    fun collectUrlSignalsFromMobileApp(payload: MobileBackgroundSignalPayload) { println("mocked"); }

    fun dispatchBackgroundSignalsToPipeline(payload: MobileBackgroundSignalPayload) { println("mocked"); }

    fun linkBackgroundServiceSignalToOnDeviceFilter(
        payload: MobileBackgroundSignalPayload,
    ): OnDeviceFilterPipelineResult {
        // mocked
        println("mocked");
    }

    fun linkSmsSignalToOnDeviceFilter(
        payload: MobileBackgroundSignalPayload,
    ): OnDeviceFilterPipelineResult {
        // mocked
        println("mocked");
    }

    fun linkCallSignalToOnDeviceFilter(
        payload: MobileBackgroundSignalPayload,
    ): OnDeviceFilterPipelineResult {
        // mocked
        println("mocked");
    }

    fun linkUrlSignalToOnDeviceFilter(
        payload: MobileBackgroundSignalPayload,
    ): OnDeviceFilterPipelineResult {
        // mocked
        println("mocked");
    }

    override suspend fun doWork(): Result {
        // mocked
        return Result.success()
    }
}
