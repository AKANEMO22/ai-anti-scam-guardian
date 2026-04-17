package com.sixseven.antiscam

import android.app.Application
import com.sixseven.antiscam.core.ml.OnDeviceFilterProvider

class GuardianApp : Application() {
    override fun onCreate() {
        super.onCreate()
        // Initialize On-Device filter provider (TFLite model loader). If a
        // model asset is provided in the core/ml assets directory it will be
        // loaded, otherwise the provider uses a safe heuristic fallback.
        OnDeviceFilterProvider.init(this)
    }
}
