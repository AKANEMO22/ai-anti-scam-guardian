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
        // TODO: entrypoint for Mobile App -> Background Service signal handoff.
        throw NotImplementedError("Stub only")
    }

    fun collectSmsSignalsFromMobileApp(payload: MobileBackgroundSignalPayload) {
        // TODO: collect and pre-process SMS signal branch.
    }

    fun collectCallSignalsFromMobileApp(payload: MobileBackgroundSignalPayload) {
        // TODO: collect and pre-process CALL/PHONE signal branch.
    }

    fun collectUrlSignalsFromMobileApp(payload: MobileBackgroundSignalPayload) {
        // TODO: collect and pre-process URL signal branch.
    }

    fun dispatchBackgroundSignalsToPipeline(payload: MobileBackgroundSignalPayload) {
        // TODO: dispatch normalized background signal to downstream pipeline use case.
    }

    fun linkBackgroundServiceSignalToOnDeviceFilter(
        payload: MobileBackgroundSignalPayload,
    ): OnDeviceFilterPipelineResult {
        // TODO: route generic signal from Background Service to TFLite On-device Filter.
        throw NotImplementedError("Stub only")
    }

    fun linkSmsSignalToOnDeviceFilter(
        payload: MobileBackgroundSignalPayload,
    ): OnDeviceFilterPipelineResult {
        // TODO: route SMS signal branch to TFLite On-device Filter.
        throw NotImplementedError("Stub only")
    }

    fun linkCallSignalToOnDeviceFilter(
        payload: MobileBackgroundSignalPayload,
    ): OnDeviceFilterPipelineResult {
        // TODO: route CALL signal branch to TFLite On-device Filter.
        throw NotImplementedError("Stub only")
    }

    fun linkUrlSignalToOnDeviceFilter(
        payload: MobileBackgroundSignalPayload,
    ): OnDeviceFilterPipelineResult {
        // TODO: route URL signal branch to TFLite On-device Filter.
        throw NotImplementedError("Stub only")
    }

    override suspend fun doWork(): Result {
        // TODO: schedule and run Background Service SMS/CALL/URL -> TFLite On-device Filter flow.
        return Result.success()
    }
}
