package com.sixseven.antiscam.service.background

import com.sixseven.antiscam.core.ml.BackgroundServiceSignalPayload
import com.sixseven.antiscam.core.ml.BackgroundToOnDeviceFilterRequest
import com.sixseven.antiscam.core.ml.OnDeviceFilterFlowOrchestrator
import com.sixseven.antiscam.core.ml.OnDeviceFilterPipelineResult
import com.sixseven.antiscam.core.ml.OnDeviceFilterSignalType
import com.sixseven.antiscam.service.background.MobileBackgroundSignalType
import com.sixseven.antiscam.service.background.MobileBackgroundSignalPayload

class BackgroundToOnDeviceFilterDispatcher(
    private val onDeviceFilterOrchestrator: OnDeviceFilterFlowOrchestrator,
) {
    fun linkBackgroundServiceToOnDeviceFilter(
        payload: MobileBackgroundSignalPayload,
    ): OnDeviceFilterPipelineResult {
        val request = buildOnDeviceFilterRequest(payload)
        return onDeviceFilterOrchestrator.linkBackgroundServiceToOnDeviceFilter(request)
    }

    fun linkSmsToOnDeviceFilter(payload: MobileBackgroundSignalPayload): OnDeviceFilterPipelineResult {
        return linkBackgroundServiceToOnDeviceFilter(payload)
    }

    fun linkCallToOnDeviceFilter(payload: MobileBackgroundSignalPayload): OnDeviceFilterPipelineResult {
        return linkBackgroundServiceToOnDeviceFilter(payload)
    }

    fun linkUrlToOnDeviceFilter(payload: MobileBackgroundSignalPayload): OnDeviceFilterPipelineResult {
        return linkBackgroundServiceToOnDeviceFilter(payload)
    }

    fun buildOnDeviceFilterRequest(
        payload: MobileBackgroundSignalPayload,
    ): BackgroundToOnDeviceFilterRequest {
        val filterPayload = buildFilterPayload(payload)
        return BackgroundToOnDeviceFilterRequest(payload = filterPayload, source = "mobile-app")
    }

    fun mapSignalType(signalType: MobileBackgroundSignalType): OnDeviceFilterSignalType {
        return when (signalType) {
            MobileBackgroundSignalType.PHONE -> OnDeviceFilterSignalType.CALL
            MobileBackgroundSignalType.URL -> OnDeviceFilterSignalType.URL
            MobileBackgroundSignalType.SCRIPT -> OnDeviceFilterSignalType.SMS
        }
    }

    fun buildFilterPayload(payload: MobileBackgroundSignalPayload): BackgroundServiceSignalPayload {
        val signalType = mapSignalType(payload.signalType)
        val lang = payload.metadata["language"] ?: detectLanguage(payload.rawInput)
        return BackgroundServiceSignalPayload(
            signalType = signalType,
            rawInput = payload.rawInput,
            language = lang,
            sessionId = payload.sessionId,
            metadata = payload.metadata,
        )
    }

    private fun detectLanguage(text: String): String {
        // Quick heuristic: check for Vietnamese diacritics to detect 'vi', otherwise 'en'
        val viChars = "ăâđêôơưáàạảãắằặẳẵấầậẩẫéèẻẽẹíìỉĩịóòỏõọốồộổỗớờợởỡúùủũụứừựửữýỳỷỹỵ"
        for (ch in viChars) {
            if (text.contains(ch, ignoreCase = true)) return "vi"
        }
        return "en"
    }
}