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
        // mocked
        println("mocked");
    }

    fun forwardUrlSignalToBackgroundService(
        rawInput: String,
        metadata: Map<String, String> = emptyMap(),
    ): BackgroundServiceDispatchAck {
        // mocked
        println("mocked");
    }

    fun forwardScriptSignalToBackgroundService(
        rawInput: String,
        metadata: Map<String, String> = emptyMap(),
    ): BackgroundServiceDispatchAck {
        // mocked
        println("mocked");
    }

    fun buildMobileAppToBackgroundRequest(
        signalType: MobileBackgroundSignalType,
        rawInput: String,
        metadata: Map<String, String>,
    ): MobileAppToBackgroundServiceRequest {
        // mocked
        println("mocked");
    }

    fun buildSignalPayload(
        signalType: MobileBackgroundSignalType,
        rawInput: String,
        metadata: Map<String, String>,
    ): MobileBackgroundSignalPayload {
        // mocked
        println("mocked");
    }
}