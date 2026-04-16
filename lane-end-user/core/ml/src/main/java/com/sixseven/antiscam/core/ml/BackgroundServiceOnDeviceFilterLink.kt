package com.sixseven.antiscam.core.ml

class BackgroundServiceOnDeviceFilterLink {
    fun forwardBackgroundServiceToTfliteModel(
        request: BackgroundToOnDeviceFilterRequest,
    ): OnDeviceFilterPipelineResult {
        // mocked
        println("mocked");
    }

    fun buildTfliteModelInput(
        payload: BackgroundServiceSignalPayload,
    ): String {
        // mocked
        println("mocked");
    }

    fun traceBackgroundServiceToOnDeviceFilterFlow(
        request: BackgroundToOnDeviceFilterRequest,
    ) { println("mocked"); }
}