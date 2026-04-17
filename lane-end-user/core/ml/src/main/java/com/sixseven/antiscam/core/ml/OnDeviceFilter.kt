package com.sixseven.antiscam.core.ml

import android.content.Context
import android.util.Log
import org.tensorflow.lite.Interpreter
import java.io.FileInputStream
import java.nio.MappedByteBuffer
import java.nio.channels.FileChannel

data class OnDeviceFilterResult(
    val suspicious: Boolean,
    val maskedPayload: String,
    val confidence: Float
)

interface OnDeviceFilter {
    fun run(rawInput: String): OnDeviceFilterResult
}

/**
 * TFLite-backed on-device filter with graceful fallback to a lightweight heuristic.
 *
 * Notes:
 * - Attempts to load a model asset `scam_detector.tflite` from the module assets.
 * - If the model cannot be loaded or inference fails, the implementation falls back to
 *   the original keyword-based heuristic to avoid breaking runtime behavior.
 */
class TFLiteOnDeviceFilter private constructor(
    private val interpreter: Interpreter?
) : OnDeviceFilter {

    override fun run(rawInput: String): OnDeviceFilterResult {
        // Try model inference if interpreter available
        try {
            interpreter?.let { interp ->
                val inputTensor = interp.getInputTensor(0)
                val shape = inputTensor.shape() // e.g., [1, 128]
                val vectorLen = if (shape.size >= 2) shape[1] else 128

                // Build float input vector from raw text (simple hashing tokenization)
                val inputArray = Array(1) { FloatArray(vectorLen) }
                val features = textToFloatVector(rawInput, vectorLen)
                for (i in 0 until vectorLen.coerceAtMost(features.size)) {
                    inputArray[0][i] = features[i]
                }

                // Prepare output buffer (best-effort: expect single score)
                val outShape = interp.getOutputTensor(0).shape()
                val outLen = if (outShape.size >= 2) outShape[1] else 1
                val outputArray = Array(1) { FloatArray(outLen) }

                interp.run(inputArray, outputArray)

                val score = outputArray.getOrNull(0)?.getOrNull(0) ?: -1f
                val confidence = when {
                    score < 0f -> 0f
                    score > 1f -> score.coerceAtMost(1f)
                    else -> score
                }
                val suspicious = confidence >= 0.5f
                return OnDeviceFilterResult(suspicious, maskSensitive(rawInput), confidence)
            }
        } catch (e: Exception) {
            Log.w("TFLiteOnDeviceFilter", "Model inference failed, falling back to heuristic: ${e.message}")
        }

        // Fallback heuristic (previous behavior)
        val lowered = rawInput.lowercase()
        val suspicious = listOf("chuyen tien", "otp", "verify", "urgent").any { lowered.contains(it) }
        val masked = maskSensitive(rawInput)
        val confidence = if (suspicious) 0.82f else 0.21f
        return OnDeviceFilterResult(suspicious = suspicious, maskedPayload = masked, confidence = confidence)
    }

    private fun maskSensitive(text: String): String {
        return text.replace(Regex("\\d{6,}"), "******")
    }

    private fun textToFloatVector(text: String, dim: Int): FloatArray {
        val arr = FloatArray(dim)
        val tokens = text
            .lowercase()
            .split(Regex("\\s+"))
            .filter { it.isNotBlank() }

        var idx = 0
        for (tok in tokens) {
            if (idx >= dim) break
            // simple stable hash -> float in [0,1]
            val h = tok.hashCode().toLong() and 0xffffffffL
            arr[idx] = ((h % 1000L).toFloat() / 1000f)
            idx++
        }
        return arr
    }

    companion object {
        private const val DEFAULT_MODEL_ASSET = "scam_detector.tflite"

        fun createWithContext(context: Context, modelAssetName: String = DEFAULT_MODEL_ASSET): TFLiteOnDeviceFilter {
            return try {
                val buffer = loadModelFile(context, modelAssetName)
                val interpreter = Interpreter(buffer)
                TFLiteOnDeviceFilter(interpreter)
            } catch (e: Exception) {
                Log.w("TFLiteOnDeviceFilter", "Failed to load TFLite model: ${e.message}")
                createFallback()
            }
        }

        fun createFromFile(file: java.io.File): TFLiteOnDeviceFilter {
            return try {
                FileInputStream(file).use { input ->
                    val channel: FileChannel = input.channel
                    val buffer = channel.map(FileChannel.MapMode.READ_ONLY, 0, file.length())
                    val interpreter = Interpreter(buffer)
                    TFLiteOnDeviceFilter(interpreter)
                }
            } catch (e: Exception) {
                Log.w("TFLiteOnDeviceFilter", "Failed to load TFLite model from file: ${e.message}")
                createFallback()
            }
        }

        fun createFallback(): TFLiteOnDeviceFilter = TFLiteOnDeviceFilter(null)

        private fun loadModelFile(context: Context, assetPath: String): MappedByteBuffer {
            val afd = context.assets.openFd(assetPath)
            FileInputStream(afd.fileDescriptor).use { input ->
                val channel: FileChannel = input.channel
                return channel.map(FileChannel.MapMode.READ_ONLY, afd.startOffset, afd.length)
            }
        }
    }
}

