package com.sixseven.antiscam.core.ml

class BackgroundServiceOnDeviceFilterLink {
    fun forwardBackgroundServiceToTfliteModel(
        request: BackgroundToOnDeviceFilterRequest,
    ): OnDeviceFilterPipelineResult {
        // TODO: forward normalized payload into TFLite On-device Filter stage.
        throw NotImplementedError("Stub only")
    }

    fun buildTfliteModelInput(
        payload: BackgroundServiceSignalPayload,
    ): String {
        // TODO: build model input string/tensor payload for TFLite inference.
        throw NotImplementedError("Stub only")
    }

    fun traceBackgroundServiceToOnDeviceFilterFlow(
        request: BackgroundToOnDeviceFilterRequest,
    ) {
        // TODO: emit trace point for Background Service -> TFLite On-device Filter flow.
    }
}