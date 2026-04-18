package com.sixseven.antiscam.background

import com.sixseven.antiscam.service.background.BackgroundServiceDispatchAck
import com.sixseven.antiscam.service.background.MobileAppToBackgroundServiceRequest
import com.sixseven.antiscam.service.background.MobileBackgroundSignalPayload
import com.sixseven.antiscam.service.background.MobileBackgroundSignalType

class MobileAppBackgroundServiceBridge {
    fun forwardPhoneSignalToBackgroundService(
        rawInput: String,
        metadata: Map<String, String> = emptyMap(),
    ): BackgroundServiceDispatchAck {
        // TODO: create PHONE request and enqueue into background service lane.
        throw NotImplementedError("Stub only")
    }

    fun forwardUrlSignalToBackgroundService(
        rawInput: String,
        metadata: Map<String, String> = emptyMap(),
    ): BackgroundServiceDispatchAck {
        // TODO: create URL request and enqueue into background service lane.
        throw NotImplementedError("Stub only")
    }

    fun forwardScriptSignalToBackgroundService(
        rawInput: String,
        metadata: Map<String, String> = emptyMap(),
    ): BackgroundServiceDispatchAck {
        // TODO: create SCRIPT request and enqueue into background service lane.
        throw NotImplementedError("Stub only")
    }

    fun buildMobileAppToBackgroundRequest(
        signalType: MobileBackgroundSignalType,
        rawInput: String,
        metadata: Map<String, String>,
    ): MobileAppToBackgroundServiceRequest {
        // TODO: map app-side data into shared background-service request contract.
        throw NotImplementedError("Stub only")
    }

    fun buildSignalPayload(
        signalType: MobileBackgroundSignalType,
        rawInput: String,
        metadata: Map<String, String>,
    ): MobileBackgroundSignalPayload {
        // TODO: build payload object reused across SMS/CALL/URL branches.
        throw NotImplementedError("Stub only")
    }
}