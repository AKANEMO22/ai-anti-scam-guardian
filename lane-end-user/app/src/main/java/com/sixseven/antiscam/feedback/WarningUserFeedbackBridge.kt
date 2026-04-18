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
        // TODO: bridge warning user feedback payload into feedback-sync request.
        throw NotImplementedError("Stub only")
    }

    fun buildFeedbackSyncSubmissionPayload(
        payload: UserFeedbackSubmissionPayload,
    ): FeedbackSyncSubmissionPayload {
        // TODO: map warning payload fields into feedback-sync payload contract.
        throw NotImplementedError("Stub only")
    }

    fun mapFeedbackLabel(label: WarningUserFeedbackLabel): FeedbackSyncLabel {
        // TODO: map warning label enum to feedback-sync enum.
        throw NotImplementedError("Stub only")
    }

    fun mapFeedbackSignalType(signalType: WarningFeedbackSignalType): FeedbackSyncSignalType {
        // TODO: map warning signal type to feedback-sync phone/url/script channel.
        throw NotImplementedError("Stub only")
    }
}