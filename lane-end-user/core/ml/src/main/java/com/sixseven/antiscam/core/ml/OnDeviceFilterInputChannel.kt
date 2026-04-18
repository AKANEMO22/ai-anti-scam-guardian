package com.sixseven.antiscam.core.ml

class OnDeviceFilterInputChannel {
    fun receiveFromBackgroundService(
        request: BackgroundToOnDeviceFilterRequest,
    ): BackgroundServiceSignalPayload {
        // For now, the background request contract already contains the payload
        // used by the on-device filter stage. Return it directly and allow
        // normalization to adjust if needed.
        return request.payload
    }

    fun normalizeOnDeviceFilterPayload(
        payload: BackgroundServiceSignalPayload,
    ): BackgroundServiceSignalPayload {
        // Minimal normalization: trim whitespace and limit length to avoid
        // over-sized inputs for small TFLite models.
        val cleaned = payload.rawInput.trim()
        val snippet = if (cleaned.length > 1024) cleaned.take(1024) else cleaned
        return payload.copy(rawInput = snippet)
    }

    fun validateOnDeviceFilterPayload(payload: BackgroundServiceSignalPayload) {
        // Basic validation: ensure rawInput is non-empty.
        if (payload.rawInput.isBlank()) {
            throw IllegalArgumentException("OnDeviceFilter payload rawInput is empty")
        }
    }
}