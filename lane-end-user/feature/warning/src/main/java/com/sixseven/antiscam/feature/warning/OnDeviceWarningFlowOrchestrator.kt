package com.sixseven.antiscam.feature.warning

import com.sixseven.antiscam.core.ml.OnDeviceFilterSignalType

class OnDeviceWarningFlowOrchestrator(
    private val channel: OnDeviceWarningFlowChannel,
    private val link: OnDeviceWarningExplanationLink,
) {
    fun linkOnDeviceFilterToUiWarningExplanation(
        request: OnDeviceFilterToUiWarningRequest,
    ): WarningDetailUiState {
        // TODO: orchestrate TFLite On-device Filter -> UI warning explanation flow.
        throw NotImplementedError("Stub only")
    }

    fun linkSmsWarningExplanation(
        request: OnDeviceFilterToUiWarningRequest,
    ): WarningDetailUiState {
        // TODO: orchestrate SMS warning explanation branch.
        throw NotImplementedError("Stub only")
    }

    fun linkCallWarningExplanation(
        request: OnDeviceFilterToUiWarningRequest,
    ): WarningDetailUiState {
        // TODO: orchestrate CALL warning explanation branch.
        throw NotImplementedError("Stub only")
    }

    fun linkUrlWarningExplanation(
        request: OnDeviceFilterToUiWarningRequest,
    ): WarningDetailUiState {
        // TODO: orchestrate URL warning explanation branch.
        throw NotImplementedError("Stub only")
    }

    fun classifyWarningBranch(signalType: OnDeviceFilterSignalType): OnDeviceFilterSignalType {
        // TODO: classify warning branch based on signal type before rendering explanation.
        throw NotImplementedError("Stub only")
    }
}