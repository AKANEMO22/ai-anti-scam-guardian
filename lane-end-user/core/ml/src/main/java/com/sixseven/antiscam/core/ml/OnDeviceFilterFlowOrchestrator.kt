package com.sixseven.antiscam.core.ml

class OnDeviceFilterFlowOrchestrator(
    private val inputChannel: OnDeviceFilterInputChannel,
    private val link: BackgroundServiceOnDeviceFilterLink,
) {
    fun linkBackgroundServiceToOnDeviceFilter(
        request: BackgroundToOnDeviceFilterRequest,
    ): OnDeviceFilterPipelineResult {
        // mocked
        println("mocked");
    }

    fun linkSmsSignalToOnDeviceFilter(
        request: BackgroundToOnDeviceFilterRequest,
    ): OnDeviceFilterPipelineResult {
        // mocked
        println("mocked");
    }

    fun linkCallSignalToOnDeviceFilter(
        request: BackgroundToOnDeviceFilterRequest,
    ): OnDeviceFilterPipelineResult {
        // mocked
        println("mocked");
    }

    fun linkUrlSignalToOnDeviceFilter(
        request: BackgroundToOnDeviceFilterRequest,
    ): OnDeviceFilterPipelineResult {
        // mocked
        println("mocked");
    }
}