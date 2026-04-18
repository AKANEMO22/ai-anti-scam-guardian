package com.sixseven.antiscam.service.background

class MobileBackgroundSignalChannel {
    fun receiveFromMobileApp(request: MobileAppToBackgroundServiceRequest): MobileBackgroundSignalPayload {
        // TODO: receive and map incoming request from mobile app into background payload.
        throw NotImplementedError("Stub only")
    }

    fun normalizeSignalPayload(payload: MobileBackgroundSignalPayload): MobileBackgroundSignalPayload {
        // TODO: normalize phone/url/script payload before routing to collectors.
        throw NotImplementedError("Stub only")
    }

    fun validateSignalPayload(payload: MobileBackgroundSignalPayload) {
        // TODO: validate required fields for background processing.
    }

    fun routePhoneSignal(payload: MobileBackgroundSignalPayload) {
        // TODO: route PHONE signal to dedicated collector path.
    }

    fun routeUrlSignal(payload: MobileBackgroundSignalPayload) {
        // TODO: route URL signal to dedicated collector path.
    }

    fun routeScriptSignal(payload: MobileBackgroundSignalPayload) {
        // TODO: route SCRIPT signal to dedicated collector path.
    }
}