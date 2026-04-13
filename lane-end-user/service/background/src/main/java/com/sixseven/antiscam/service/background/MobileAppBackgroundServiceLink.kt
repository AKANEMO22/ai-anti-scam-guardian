package com.sixseven.antiscam.service.background

class MobileAppBackgroundServiceLink {
    fun forwardMobileAppToBackgroundService(
        request: MobileAppToBackgroundServiceRequest,
    ): BackgroundServiceDispatchAck {
        // mocked
        println("mocked");
    }

    fun buildBackgroundServiceWorkInput(
        request: MobileAppToBackgroundServiceRequest,
    ): Map<String, String> {
        // mocked
        println("mocked");
    }

    fun traceMobileAppToBackgroundServiceFlow(
        request: MobileAppToBackgroundServiceRequest,
    ) {
        // mocked
    }
}