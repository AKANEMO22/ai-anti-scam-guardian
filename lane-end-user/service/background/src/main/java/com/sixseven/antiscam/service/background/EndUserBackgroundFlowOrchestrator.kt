package com.sixseven.antiscam.service.background

import com.sixseven.antiscam.core.ml.OnDeviceFilterPipelineResult

class EndUserBackgroundFlowOrchestrator(
    private val signalChannel: MobileBackgroundSignalChannel,
    private val link: MobileAppBackgroundServiceLink,
    private val onDeviceFilterDispatcher: BackgroundToOnDeviceFilterDispatcher,
) {
    fun linkMobileAppToBackgroundService(
        request: MobileAppToBackgroundServiceRequest,
    ): BackgroundServiceDispatchAck {
        // mocked
        println("mocked");
    }

    fun linkBackgroundServicePhoneSignal(payload: MobileBackgroundSignalPayload) {
        // mocked
    }

    fun linkBackgroundServiceUrlSignal(payload: MobileBackgroundSignalPayload) {
        // mocked
    }

    fun linkBackgroundServiceScriptSignal(payload: MobileBackgroundSignalPayload) {
        // mocked
    }

    fun linkBackgroundServiceToOnDeviceFilter(
        payload: MobileBackgroundSignalPayload,
    ): OnDeviceFilterPipelineResult {
        // mocked
        println("mocked");
    }

    fun linkBackgroundServiceSmsToOnDeviceFilter(
        payload: MobileBackgroundSignalPayload,
    ): OnDeviceFilterPipelineResult {
        // mocked
        println("mocked");
    }

    fun linkBackgroundServiceCallToOnDeviceFilter(
        payload: MobileBackgroundSignalPayload,
    ): OnDeviceFilterPipelineResult {
        // mocked
        println("mocked");
    }

    fun linkBackgroundServiceUrlToOnDeviceFilter(
        payload: MobileBackgroundSignalPayload,
    ): OnDeviceFilterPipelineResult {
        // mocked
        println("mocked");
    }
}