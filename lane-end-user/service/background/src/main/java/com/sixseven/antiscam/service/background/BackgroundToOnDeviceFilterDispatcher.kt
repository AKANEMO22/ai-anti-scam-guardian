package com.sixseven.antiscam.service.background

import com.sixseven.antiscam.core.ml.BackgroundServiceSignalPayload
import com.sixseven.antiscam.core.ml.BackgroundToOnDeviceFilterRequest
import com.sixseven.antiscam.core.ml.OnDeviceFilterFlowOrchestrator
import com.sixseven.antiscam.core.ml.OnDeviceFilterPipelineResult
import com.sixseven.antiscam.core.ml.OnDeviceFilterSignalType

class BackgroundToOnDeviceFilterDispatcher(
    private val onDeviceFilterOrchestrator: OnDeviceFilterFlowOrchestrator,
) {
    fun linkBackgroundServiceToOnDeviceFilter(
        payload: MobileBackgroundSignalPayload,
    ): OnDeviceFilterPipelineResult {
        // mocked
        println("mocked");
    }

    fun linkSmsToOnDeviceFilter(payload: MobileBackgroundSignalPayload): OnDeviceFilterPipelineResult {
        // mocked
        println("mocked");
    }

    fun linkCallToOnDeviceFilter(payload: MobileBackgroundSignalPayload): OnDeviceFilterPipelineResult {
        // mocked
        println("mocked");
    }

    fun linkUrlToOnDeviceFilter(payload: MobileBackgroundSignalPayload): OnDeviceFilterPipelineResult {
        // mocked
        println("mocked");
    }

    fun buildOnDeviceFilterRequest(
        payload: MobileBackgroundSignalPayload,
    ): BackgroundToOnDeviceFilterRequest {
        // mocked
        println("mocked");
    }

    fun mapSignalType(signalType: MobileBackgroundSignalType): OnDeviceFilterSignalType {
        // mocked
        println("mocked");
    }

    fun buildFilterPayload(payload: MobileBackgroundSignalPayload): BackgroundServiceSignalPayload {
        // mocked
        println("mocked");
    }
}