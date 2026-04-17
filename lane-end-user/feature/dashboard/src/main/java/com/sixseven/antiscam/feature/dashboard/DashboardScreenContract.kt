package com.sixseven.antiscam.feature.dashboard

data class DashboardUiState(
    val todayScans: Int,
    val highRiskAlerts: Int,
    val latestExplanation: String,
    val riskGauge: Int
)
