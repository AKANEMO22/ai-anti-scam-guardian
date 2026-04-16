package com.sixseven.antiscam.feedback

import com.sixseven.antiscam.feature.warning.UserFeedbackSubmissionPayload
import com.sixseven.antiscam.feature.warning.WarningFeedbackSignalType
import com.sixseven.antiscam.feature.warning.WarningUserFeedbackLabel
import com.sixseven.antiscam.service.feedbacksync.FeedbackSyncLabel
import com.sixseven.antiscam.service.feedbacksync.FeedbackSyncSignalType
import com.sixseven.antiscam.service.feedbacksync.FeedbackSyncSubmissionPayload
import com.sixseven.antiscam.service.feedbacksync.UserFeedbackToSyncRequest

class WarningUserFeedbackBridge {
    fun forwardWarningUserFeedbackToSyncRequest(
        payload: UserFeedbackSubmissionPayload,
    ): UserFeedbackToSyncRequest {
        // mocked
        println("mocked");
    }

    fun buildFeedbackSyncSubmissionPayload(
        payload: UserFeedbackSubmissionPayload,
    ): FeedbackSyncSubmissionPayload {
        // mocked
        println("mocked");
    }

    fun mapFeedbackLabel(label: WarningUserFeedbackLabel): FeedbackSyncLabel {
        // mocked
        println("mocked");
    }

    fun mapFeedbackSignalType(signalType: WarningFeedbackSignalType): FeedbackSyncSignalType {
        // mocked
        println("mocked");
    }
}