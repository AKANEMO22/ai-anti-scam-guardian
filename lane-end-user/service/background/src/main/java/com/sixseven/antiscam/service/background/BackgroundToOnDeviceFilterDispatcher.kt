package com.sixseven.antiscam.service.background

import com.sixseven.antiscam.core.ml.BackgroundServiceSignalPayload
import com.sixseven.antiscam.core.ml.BackgroundToOnDeviceFilterRequest
import com.sixseven.antiscam.core.ml.OnDeviceFilterFlowOrchestrator
import com.sixseven.antiscam.core.ml.OnDeviceFilterPipelineResult
import com.sixseven.antiscam.core.ml.OnDeviceFilterSignalType

class BackgroundToOnDeviceFilterDispatcher(
    private val onDeviceFilterOrchestrator: OnDeviceFilterFlowOrchestrator,
) {
    fun linkBackgroundServiceToOnDeviceFilter(
        payload: MobileBackgroundSignalPayload,
    ): OnDeviceFilterPipelineResult {
        // TODO: dispatch background payload to generic On-device filter flow.
        throw NotImplementedError("Stub only")
    }

    fun linkSmsToOnDeviceFilter(payload: MobileBackgroundSignalPayload): OnDeviceFilterPipelineResult {
        // TODO: dispatch SMS branch to On-device filter orchestrator.
        throw NotImplementedError("Stub only")
    }

    fun linkCallToOnDeviceFilter(payload: MobileBackgroundSignalPayload): OnDeviceFilterPipelineResult {
        // TODO: dispatch CALL branch to On-device filter orchestrator.
        throw NotImplementedError("Stub only")
    }

    fun linkUrlToOnDeviceFilter(payload: MobileBackgroundSignalPayload): OnDeviceFilterPipelineResult {
        // TODO: dispatch URL branch to On-device filter orchestrator.
        throw NotImplementedError("Stub only")
    }

    fun buildOnDeviceFilterRequest(
        payload: MobileBackgroundSignalPayload,
    ): BackgroundToOnDeviceFilterRequest {
        // TODO: map background payload to On-device filter request contract.
        throw NotImplementedError("Stub only")
    }

    fun mapSignalType(signalType: MobileBackgroundSignalType): OnDeviceFilterSignalType {
        // TODO: map PHONE/URL/SCRIPT into SMS/CALL/URL filter channels.
        throw NotImplementedError("Stub only")
    }

    fun buildFilterPayload(payload: MobileBackgroundSignalPayload): BackgroundServiceSignalPayload {
        // TODO: create filter payload consumed by core ml module.
        throw NotImplementedError("Stub only")
    }
}