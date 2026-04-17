package com.sixseven.antiscam.core.ml

class OnDeviceFilterFlowOrchestrator(
    private val inputChannel: OnDeviceFilterInputChannel,
    private val link: BackgroundServiceOnDeviceFilterLink,
) {
    fun linkBackgroundServiceToOnDeviceFilter(
        request: BackgroundToOnDeviceFilterRequest,
    ): OnDeviceFilterPipelineResult {
        val payload = inputChannel.receiveFromBackgroundService(request)
        inputChannel.validateOnDeviceFilterPayload(payload)
        val normalized = inputChannel.normalizeOnDeviceFilterPayload(payload)
        val nextReq = BackgroundToOnDeviceFilterRequest(payload = normalized, source = request.source)
        return link.forwardBackgroundServiceToTfliteModel(nextReq)
    }

    fun linkSmsSignalToOnDeviceFilter(
        request: BackgroundToOnDeviceFilterRequest,
    ): OnDeviceFilterPipelineResult {
        return linkBackgroundServiceToOnDeviceFilter(request)
    }

    fun linkCallSignalToOnDeviceFilter(
        request: BackgroundToOnDeviceFilterRequest,
    ): OnDeviceFilterPipelineResult {
        return linkBackgroundServiceToOnDeviceFilter(request)
    }

    fun linkUrlSignalToOnDeviceFilter(
        request: BackgroundToOnDeviceFilterRequest,
    ): OnDeviceFilterPipelineResult {
        return linkBackgroundServiceToOnDeviceFilter(request)
    }
}