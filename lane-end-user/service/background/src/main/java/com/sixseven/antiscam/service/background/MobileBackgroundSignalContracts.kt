package com.sixseven.antiscam.service.background

enum class MobileBackgroundSignalType {
    PHONE,
    URL,
    SCRIPT,
}

data class MobileBackgroundSignalPayload(
    val signalType: MobileBackgroundSignalType,
    val rawInput: String,
    val sessionId: String? = null,
    val metadata: Map<String, String> = emptyMap(),
)

data class MobileAppToBackgroundServiceRequest(
    val payload: MobileBackgroundSignalPayload,
    val triggerSource: String = "mobile-app",
)

data class BackgroundServiceDispatchAck(
    val accepted: Boolean,
    val signalType: MobileBackgroundSignalType,
    val message: String = "",
)