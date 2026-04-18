package com.sixseven.antiscam.core.network

import retrofit2.http.Body
import retrofit2.http.Header
import retrofit2.http.POST

/**
 * Concrete implementation of [CloudApi] using Retrofit.
 * This serves as the reference network adapter for the mobile team.
 */
interface RetrofitCloudApi : CloudApi {

    @POST("v1/signals/analyze")
    override suspend fun analyzeSignal(
        @Body request: SignalRequest
    ): RiskResponse

    @POST("v1/feedback")
    override suspend fun submitFeedback(
        @Body request: FeedbackEvent
    ): FeedbackResponse

    /**
     * Helper method to call analyzeSignal with an Authorization header.
     */
    @POST("v1/signals/analyze")
    suspend fun analyzeSignalWithAuth(
        @Header("Authorization") token: String,
        @Body request: SignalRequest
    ): RiskResponse

    @POST("v1/feedback")
    suspend fun submitFeedbackWithAuth(
        @Header("Authorization") token: String,
        @Body request: FeedbackEvent
    ): FeedbackResponse
}

/**
 * Extension function to facilitate Bearer token injection.
 */
class AuthenticatedCloudApi(
    private val delegate: RetrofitCloudApi,
    private val token: String
) : CloudApi {
    override suspend fun analyzeSignal(request: SignalRequest): RiskResponse {
        return delegate.analyzeSignalWithAuth("Bearer $token", request)
    }

    override suspend fun submitFeedback(request: FeedbackEvent): FeedbackResponse {
        return delegate.submitFeedbackWithAuth("Bearer $token", request)
    }
}
