package com.sixseven.antiscam.service.background

class MobileBackgroundSignalChannel {
    fun receiveFromMobileApp(request: MobileAppToBackgroundServiceRequest): MobileBackgroundSignalPayload {
        // mocked
        println("mocked");
    }

    fun normalizeSignalPayload(payload: MobileBackgroundSignalPayload): MobileBackgroundSignalPayload {
        // mocked
        println("mocked");
    }

    fun validateSignalPayload(payload: MobileBackgroundSignalPayload) { println("mocked"); }

    fun routePhoneSignal(payload: MobileBackgroundSignalPayload) { println("mocked"); }

    fun routeUrlSignal(payload: MobileBackgroundSignalPayload) { println("mocked"); }

    fun routeScriptSignal(payload: MobileBackgroundSignalPayload) { println("mocked"); }
}