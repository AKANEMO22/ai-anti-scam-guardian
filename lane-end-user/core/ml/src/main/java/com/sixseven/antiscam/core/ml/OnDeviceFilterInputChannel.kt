package com.sixseven.antiscam.core.ml

class OnDeviceFilterInputChannel {
    fun receiveFromBackgroundService(
        request: BackgroundToOnDeviceFilterRequest,
    ): BackgroundServiceSignalPayload {
        // TODO: receive and map Background Service payload for TFLite input stage.
        throw NotImplementedError("Stub only")
    }

    fun normalizeOnDeviceFilterPayload(
        payload: BackgroundServiceSignalPayload,
    ): BackgroundServiceSignalPayload {
        // TODO: normalize SMS/CALL/URL payload before running On-device filter.
        throw NotImplementedError("Stub only")
    }

    fun validateOnDeviceFilterPayload(payload: BackgroundServiceSignalPayload) {
        // TODO: validate required input for TFLite model execution.
    }
}