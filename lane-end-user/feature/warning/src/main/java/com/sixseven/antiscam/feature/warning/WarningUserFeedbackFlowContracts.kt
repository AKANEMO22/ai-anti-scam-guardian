package com.sixseven.antiscam.feature.warning

enum class WarningUserFeedbackLabel {
    SCAM,
    SAFE,
    NOT_SURE,
}

enum class WarningFeedbackSignalType {
    PHONE,
    URL,
    SCRIPT,
}

data class UiWarningInteractionState(
    val warningState: WarningDetailUiState,
    val feedbackLabels: List<WarningUserFeedbackLabel> = listOf(
        WarningUserFeedbackLabel.SCAM,
        WarningUserFeedbackLabel.SAFE,
        WarningUserFeedbackLabel.NOT_SURE,
    ),
)

data class UiWarningExplanationToInteractRequest(
    val warningState: WarningDetailUiState,
)

data class InteractToUserFeedbackRequest(
    val interactionState: UiWarningInteractionState,
    val selectedFeedback: WarningUserFeedbackLabel,
    val note: String? = null,
    val metadata: Map<String, String> = emptyMap(),
)

data class UserFeedbackSubmissionPayload(
    val label: WarningUserFeedbackLabel,
    val signalType: WarningFeedbackSignalType = WarningFeedbackSignalType.SCRIPT,
    val score: Int,
    val explanation: String,
    val note: String? = null,
    val metadata: Map<String, String> = emptyMap(),
)