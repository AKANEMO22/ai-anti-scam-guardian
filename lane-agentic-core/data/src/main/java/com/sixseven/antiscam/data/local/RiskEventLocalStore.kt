package com.sixseven.antiscam.data.local

data class RiskEvent(
    val eventId: String,
    val sourceType: String,
    val riskScore: Int,
    val explanation: String,
    val createdAt: Long
)

interface RiskEventLocalStore {
    suspend fun insert(event: RiskEvent)
    suspend fun listLatest(limit: Int = 50): List<RiskEvent>
}
