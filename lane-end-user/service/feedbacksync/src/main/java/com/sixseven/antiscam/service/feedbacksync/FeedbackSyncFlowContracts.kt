package com.sixseven.antiscam.service.feedbacksync

enum class FeedbackSyncLabel {
    SCAM,
    SAFE,
    NOT_SURE,
}

enum class FeedbackSyncSignalType {
    PHONE,
    URL,
    SCRIPT,
}

data class FeedbackSyncSubmissionPayload(
    val label: FeedbackSyncLabel,
    val signalType: FeedbackSyncSignalType = FeedbackSyncSignalType.SCRIPT,
    val score: Int,
    val explanation: String,
    val note: String? = null,
    val metadata: Map<String, String> = emptyMap(),
)

data class FeedbackLabelPayload(
    val label: FeedbackSyncLabel,
    val signalType: FeedbackSyncSignalType,
    val score: Int,
    val explanation: String,
    val note: String? = null,
    val metadata: Map<String, String> = emptyMap(),
)

data class UserFeedbackToSyncRequest(
    val payload: FeedbackSyncSubmissionPayload,
    val source: String = "warning-ui",
)

data class UserFeedbackToFeedbackLabelRequest(
    val payload: FeedbackSyncSubmissionPayload,
)

data class FeedbackLabelToIngestionRequest(
    val payload: FeedbackLabelPayload,
)

data class FeedbackIngestionToCacheRequest(
    val payload: FeedbackLabelPayload,
)

data class FeedbackSyncAck(
    val accepted: Boolean,
    val message: String = "",
)

data class FeedbackCacheAck(
    val accepted: Boolean,
    val cacheKey: String,
    val message: String = "",
)