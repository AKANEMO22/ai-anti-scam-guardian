package com.sixseven.antiscam.warning

import com.sixseven.antiscam.core.ml.OnDeviceFilterPipelineResult
import com.sixseven.antiscam.feature.warning.OnDeviceFilterToUiWarningRequest
import com.sixseven.antiscam.feature.warning.WarningDetailUiState

class OnDeviceWarningUiBridge {
    fun forwardOnDeviceFilterResultToUiWarningExplanation(
        result: OnDeviceFilterPipelineResult,
    ): WarningDetailUiState {
        // TODO: dispatch TFLite output to warning explanation orchestrator.
        throw NotImplementedError("Stub only")
    }

    fun forwardSmsResultToUiWarningExplanation(
        result: OnDeviceFilterPipelineResult,
    ): WarningDetailUiState {
        // TODO: dispatch SMS warning result branch.
        throw NotImplementedError("Stub only")
    }

    fun forwardCallResultToUiWarningExplanation(
        result: OnDeviceFilterPipelineResult,
    ): WarningDetailUiState {
        // TODO: dispatch CALL warning result branch.
        throw NotImplementedError("Stub only")
    }

    fun forwardUrlResultToUiWarningExplanation(
        result: OnDeviceFilterPipelineResult,
    ): WarningDetailUiState {
        // TODO: dispatch URL warning result branch.
        throw NotImplementedError("Stub only")
    }

    fun buildOnDeviceFilterToUiWarningRequest(
        result: OnDeviceFilterPipelineResult,
    ): OnDeviceFilterToUiWarningRequest {
        // TODO: map filter result into request contract for warning explanation flow.
        throw NotImplementedError("Stub only")
    }
}