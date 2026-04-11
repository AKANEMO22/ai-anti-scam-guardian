package com.sixseven.antiscam.core.ml

data class OnDeviceFilterResult(
    val suspicious: Boolean,
    val maskedPayload: String,
    val confidence: Float
)

interface OnDeviceFilter {
    fun run(rawInput: String): OnDeviceFilterResult
}

class TFLiteOnDeviceFilter : OnDeviceFilter {
    override fun run(rawInput: String): OnDeviceFilterResult {
        val lowered = rawInput.lowercase()
        val suspicious = listOf("chuyen tien", "otp", "verify", "urgent").any { lowered.contains(it) }
        val masked = rawInput.replace(Regex("\\d{6,}"), "******")
        return OnDeviceFilterResult(suspicious = suspicious, maskedPayload = masked, confidence = if (suspicious) 0.82f else 0.21f)
    }
}
