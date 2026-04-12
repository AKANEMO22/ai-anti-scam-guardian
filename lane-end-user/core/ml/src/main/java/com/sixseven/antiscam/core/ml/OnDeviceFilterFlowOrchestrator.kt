package com.sixseven.antiscam.core.ml

class OnDeviceFilterFlowOrchestrator(
    private val inputChannel: OnDeviceFilterInputChannel,
    private val link: BackgroundServiceOnDeviceFilterLink,
) {
    fun linkBackgroundServiceToOnDeviceFilter(
        request: BackgroundToOnDeviceFilterRequest,
    ): OnDeviceFilterPipelineResult {
        // TODO: orchestrate Background Service -> TFLite On-device Filter handoff.
        throw NotImplementedError("Stub only")
    }

    fun linkSmsSignalToOnDeviceFilter(
        request: BackgroundToOnDeviceFilterRequest,
    ): OnDeviceFilterPipelineResult {
        // TODO: orchestrate SMS branch into On-device filter.
        throw NotImplementedError("Stub only")
    }

    fun linkCallSignalToOnDeviceFilter(
        request: BackgroundToOnDeviceFilterRequest,
    ): OnDeviceFilterPipelineResult {
        // TODO: orchestrate CALL branch into On-device filter.
        throw NotImplementedError("Stub only")
    }

    fun linkUrlSignalToOnDeviceFilter(
        request: BackgroundToOnDeviceFilterRequest,
    ): OnDeviceFilterPipelineResult {
        // TODO: orchestrate URL branch into On-device filter.
        throw NotImplementedError("Stub only")
    }
}