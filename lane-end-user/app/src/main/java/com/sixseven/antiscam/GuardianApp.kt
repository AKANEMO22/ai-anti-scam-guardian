package com.sixseven.antiscam

import android.app.Application
import com.sixseven.antiscam.core.ml.OnDeviceFilterProvider
import androidx.work.ExistingPeriodicWorkPolicy
import androidx.work.PeriodicWorkRequestBuilder
import androidx.work.WorkManager
import java.util.concurrent.TimeUnit
import com.sixseven.antiscam.service.background.BackgroundMonitorWorker

class GuardianApp : Application() {
    override fun onCreate() {
        super.onCreate()
        // Initialize On-Device filter provider (TFLite model loader).
        OnDeviceFilterProvider.init(this)

        // Schedule periodic background monitor to keep history cache up-to-date.
        try {
            val work = PeriodicWorkRequestBuilder<BackgroundMonitorWorker>(15, TimeUnit.MINUTES)
                .build()
            WorkManager.getInstance(this).enqueueUniquePeriodicWork(
                "background_monitor",
                ExistingPeriodicWorkPolicy.KEEP,
                work
            )
        } catch (_: Exception) {
            // Don't crash app if work scheduling fails on some devices.
        }
    }
}
