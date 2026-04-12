package com.sixseven.antiscam.service.background

class MobileAppBackgroundServiceLink {
    fun forwardMobileAppToBackgroundService(
        request: MobileAppToBackgroundServiceRequest,
    ): BackgroundServiceDispatchAck {
        // TODO: forward mobile app signal to background service entrypoint.
        throw NotImplementedError("Stub only")
    }

    fun buildBackgroundServiceWorkInput(
        request: MobileAppToBackgroundServiceRequest,
    ): Map<String, String> {
        // TODO: build worker input payload for phone/url/script background processing.
        throw NotImplementedError("Stub only")
    }

    fun traceMobileAppToBackgroundServiceFlow(
        request: MobileAppToBackgroundServiceRequest,
    ) {
        // TODO: emit trace event for Mobile App -> Background Service flow.
    }
}