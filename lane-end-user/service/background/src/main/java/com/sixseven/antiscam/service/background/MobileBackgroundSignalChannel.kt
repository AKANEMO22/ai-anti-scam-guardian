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

    fun validateSignalPayload(payload: MobileBackgroundSignalPayload) {
        // mocked
    }

    fun routePhoneSignal(payload: MobileBackgroundSignalPayload) {
        // mocked
    }

    fun routeUrlSignal(payload: MobileBackgroundSignalPayload) {
        // mocked
    }

    fun routeScriptSignal(payload: MobileBackgroundSignalPayload) {
        // mocked
    }
}