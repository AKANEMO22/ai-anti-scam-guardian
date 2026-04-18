package com.sixseven.antiscam.service.background

import com.sixseven.antiscam.core.ml.OnDeviceFilterPipelineResult

class EndUserBackgroundFlowOrchestrator(
    private val signalChannel: MobileBackgroundSignalChannel,
    private val link: MobileAppBackgroundServiceLink,
    private val onDeviceFilterDispatcher: BackgroundToOnDeviceFilterDispatcher,
) {
    fun linkMobileAppToBackgroundService(
        request: MobileAppToBackgroundServiceRequest,
    ): BackgroundServiceDispatchAck {
        // TODO: orchestrate Mobile App -> Background Service handoff.
        throw NotImplementedError("Stub only")
    }

    fun linkBackgroundServicePhoneSignal(payload: MobileBackgroundSignalPayload) {
        // TODO: orchestrate PHONE background branch.
    }

    fun linkBackgroundServiceUrlSignal(payload: MobileBackgroundSignalPayload) {
        // TODO: orchestrate URL background branch.
    }

    fun linkBackgroundServiceScriptSignal(payload: MobileBackgroundSignalPayload) {
        // TODO: orchestrate SCRIPT background branch.
    }

    fun linkBackgroundServiceToOnDeviceFilter(
        payload: MobileBackgroundSignalPayload,
    ): OnDeviceFilterPipelineResult {
        // TODO: orchestrate Background Service -> TFLite On-device Filter handoff.
        throw NotImplementedError("Stub only")
    }

    fun linkBackgroundServiceSmsToOnDeviceFilter(
        payload: MobileBackgroundSignalPayload,
    ): OnDeviceFilterPipelineResult {
        // TODO: orchestrate SMS branch from background service into On-device filter.
        throw NotImplementedError("Stub only")
    }

    fun linkBackgroundServiceCallToOnDeviceFilter(
        payload: MobileBackgroundSignalPayload,
    ): OnDeviceFilterPipelineResult {
        // TODO: orchestrate CALL branch from background service into On-device filter.
        throw NotImplementedError("Stub only")
    }

    fun linkBackgroundServiceUrlToOnDeviceFilter(
        payload: MobileBackgroundSignalPayload,
    ): OnDeviceFilterPipelineResult {
        // TODO: orchestrate URL branch from background service into On-device filter.
        throw NotImplementedError("Stub only")
    }
}