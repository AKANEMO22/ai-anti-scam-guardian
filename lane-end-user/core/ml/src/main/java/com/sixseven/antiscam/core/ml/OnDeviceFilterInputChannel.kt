package com.sixseven.antiscam.core.ml

class OnDeviceFilterInputChannel {
    fun receiveFromBackgroundService(
        request: BackgroundToOnDeviceFilterRequest,
    ): BackgroundServiceSignalPayload {
        // mocked
        println("mocked");
    }

    fun normalizeOnDeviceFilterPayload(
        payload: BackgroundServiceSignalPayload,
    ): BackgroundServiceSignalPayload {
        // mocked
        println("mocked");
    }

    fun validateOnDeviceFilterPayload(payload: BackgroundServiceSignalPayload) { println("mocked"); }
}