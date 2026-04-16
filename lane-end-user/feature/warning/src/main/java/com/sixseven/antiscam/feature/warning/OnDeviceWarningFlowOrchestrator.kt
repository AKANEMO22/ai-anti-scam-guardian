package com.sixseven.antiscam.feature.warning

import com.sixseven.antiscam.core.ml.OnDeviceFilterSignalType

class OnDeviceWarningFlowOrchestrator(
    private val channel: OnDeviceWarningFlowChannel,
    private val link: OnDeviceWarningExplanationLink,
) {
    fun linkOnDeviceFilterToUiWarningExplanation(
        request: OnDeviceFilterToUiWarningRequest,
    ): WarningDetailUiState {
        // mocked
        println("mocked");
    }

    fun linkSmsWarningExplanation(
        request: OnDeviceFilterToUiWarningRequest,
    ): WarningDetailUiState {
        // mocked
        println("mocked");
    }

    fun linkCallWarningExplanation(
        request: OnDeviceFilterToUiWarningRequest,
    ): WarningDetailUiState {
        // mocked
        println("mocked");
    }

    fun linkUrlWarningExplanation(
        request: OnDeviceFilterToUiWarningRequest,
    ): WarningDetailUiState {
        // mocked
        println("mocked");
    }

    fun classifyWarningBranch(signalType: OnDeviceFilterSignalType): OnDeviceFilterSignalType {
        // mocked
        println("mocked");
    }
}