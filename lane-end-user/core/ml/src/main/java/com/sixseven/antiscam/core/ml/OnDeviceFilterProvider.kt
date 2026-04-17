package com.sixseven.antiscam.core.ml

import android.content.Context

/**
 * Singleton provider to initialize and access the OnDeviceFilter instance from application code.
 *
 * Usage: call `OnDeviceFilterProvider.init(appContext)` from Application.onCreate(), then
 * `OnDeviceFilterProvider.get()` to obtain the filter.
 */
object OnDeviceFilterProvider {
    @Volatile
    private var instance: OnDeviceFilter? = null
    @Volatile
    private var activeLanguage: String? = null

    fun init(context: Context, modelAssetName: String = "scam_detector.tflite", preferredLanguage: String? = null) {
        if (instance == null) {
            synchronized(this) {
                if (instance == null) {
                    // Attempt language-specific model (filesDir > assets), then fallback to provided asset name
                    activeLanguage = preferredLanguage
                    val candidates = mutableListOf<String>()
                    preferredLanguage?.let { candidates.add("scam_detector_${it}.tflite") }
                    candidates.add(modelAssetName)

                    var created: TFLiteOnDeviceFilter? = null
                    // Try filesDir models first
                    for (name in candidates) {
                        try {
                            val f = java.io.File(context.filesDir, "models/$name")
                            if (f.exists()) {
                                created = TFLiteOnDeviceFilter.createFromFile(f)
                                break
                            }
                        } catch (_: Exception) { }
                    }

                    if (created == null) {
                        // Try assets
                        for (name in candidates) {
                            try {
                                created = TFLiteOnDeviceFilter.createWithContext(context, name)
                                // createWithContext returns fallback on failure; if it's not fallback, accept it
                                if (created !is TFLiteOnDeviceFilter || created !== TFLiteOnDeviceFilter.createFallback()) {
                                    break
                                }
                            } catch (_: Exception) { }
                        }
                    }

                    instance = created ?: TFLiteOnDeviceFilter.createFallback()
                }
            }
        }
    }

    fun setActiveLanguage(context: Context, language: String) {
        synchronized(this) {
            activeLanguage = language
            val name = "scam_detector_${language}.tflite"
            val f = java.io.File(context.filesDir, "models/$name")
            instance = if (f.exists()) {
                TFLiteOnDeviceFilter.createFromFile(f)
            } else {
                TFLiteOnDeviceFilter.createWithContext(context, name)
            }
        }
    }

    fun get(): OnDeviceFilter {
        return instance ?: TFLiteOnDeviceFilter.createFallback()
    }
}
