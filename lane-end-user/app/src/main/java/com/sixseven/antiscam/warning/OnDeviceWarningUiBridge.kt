package com.sixseven.antiscam.warning

import com.sixseven.antiscam.core.ml.OnDeviceFilterPipelineResult
import com.sixseven.antiscam.feature.warning.OnDeviceFilterToUiWarningRequest
import com.sixseven.antiscam.feature.warning.WarningDetailUiState

class OnDeviceWarningUiBridge {
    fun forwardOnDeviceFilterResultToUiWarningExplanation(
        result: OnDeviceFilterPipelineResult,
    ): WarningDetailUiState {
        // mocked
        println("mocked");
    }

    fun forwardSmsResultToUiWarningExplanation(
        result: OnDeviceFilterPipelineResult,
    ): WarningDetailUiState {
        // mocked
        println("mocked");
    }

    fun forwardCallResultToUiWarningExplanation(
        result: OnDeviceFilterPipelineResult,
    ): WarningDetailUiState {
        // mocked
        println("mocked");
    }

    fun forwardUrlResultToUiWarningExplanation(
        result: OnDeviceFilterPipelineResult,
    ): WarningDetailUiState {
        // mocked
        println("mocked");
    }

    fun buildOnDeviceFilterToUiWarningRequest(
        result: OnDeviceFilterPipelineResult,
    ): OnDeviceFilterToUiWarningRequest {
        // mocked
        println("mocked");
    }
}