package com.sixseven.antiscam.warning

import android.os.Bundle
import android.provider.Settings
import android.view.View
import android.widget.Button
import android.widget.ProgressBar
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.sixseven.antiscam.BuildConfig
import org.json.JSONObject
import java.io.BufferedReader
import java.io.InputStreamReader
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URL
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.UUID
import kotlin.concurrent.thread

class WarningDetailActivity : AppCompatActivity() {

    companion object {
        const val EXTRA_ADDRESS = "extra_address"
        const val EXTRA_BODY = "extra_body"
        const val EXTRA_TIMESTAMP = "extra_timestamp"
    }

    private lateinit var tvAddress: TextView
    private lateinit var tvTimestamp: TextView
    private lateinit var tvBody: TextView
    private lateinit var tvRisk: TextView
    private lateinit var progress: ProgressBar
    private lateinit var btnScam: Button
    private lateinit var btnNotSure: Button
    private lateinit var btnSafe: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(com.sixseven.antiscam.R.layout.activity_warning_detail)

        tvAddress = findViewById(com.sixseven.antiscam.R.id.tvWarningAddress)
        tvTimestamp = findViewById(com.sixseven.antiscam.R.id.tvWarningTimestamp)
        tvBody = findViewById(com.sixseven.antiscam.R.id.tvWarningBody)
        tvRisk = findViewById(com.sixseven.antiscam.R.id.tvRiskScore)
        progress = findViewById(com.sixseven.antiscam.R.id.progressLoading)
        btnScam = findViewById(com.sixseven.antiscam.R.id.btnMarkScam)
        btnNotSure = findViewById(com.sixseven.antiscam.R.id.btnMarkNotSure)
        btnSafe = findViewById(com.sixseven.antiscam.R.id.btnMarkSafe)

        val address = intent.getStringExtra(EXTRA_ADDRESS).orEmpty()
        val body = intent.getStringExtra(EXTRA_BODY).orEmpty()
        val timestamp = intent.getLongExtra(EXTRA_TIMESTAMP, 0L)

        tvAddress.text = address
        tvBody.text = body
        tvTimestamp.text = formatTimestamp(timestamp)

        btnScam.setOnClickListener { submitFeedback("SCAM", address, body) }
        btnNotSure.setOnClickListener { submitFeedback("NOT_SURE", address, body) }
        btnSafe.setOnClickListener { submitFeedback("SAFE", address, body) }

        // Fetch analysis to display risk summary (best-effort, non-blocking)
        fetchAnalysis(body)
    }

    private fun formatTimestamp(ts: Long): String {
        return if (ts <= 0L) "" else SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.getDefault()).format(Date(ts))
    }

    private fun fetchAnalysis(text: String) {
        progress.visibility = View.VISIBLE
        thread {
            try {
                val analyzeUrl = BuildConfig.API_GATEWAY_BASE_URL.trimEnd('/') + "/v1/signals/analyze"
                val payload = JSONObject()
                payload.put("sourceType", "SMS")
                payload.put("text", text)
                payload.put("callSessionId", JSONObject.NULL)
                payload.put("metadata", JSONObject())

                val conn = (URL(analyzeUrl).openConnection() as HttpURLConnection).apply {
                    requestMethod = "POST"
                    setRequestProperty("Content-Type", "application/json; charset=UTF-8")
                    doOutput = true
                    connectTimeout = 5000
                    readTimeout = 5000
                }

                OutputStreamWriter(conn.outputStream, "UTF-8").use { it.write(payload.toString()) }
                val code = conn.responseCode
                if (code in 200..299) {
                    val resp = BufferedReader(InputStreamReader(conn.inputStream)).use { it.readText() }
                    val json = JSONObject(resp)
                    val risk = json.optInt("riskScore", -1)
                    val explanation = json.optString("explanation", "")
                    runOnUiThread {
                        tvRisk.text = if (risk >= 0) "Risk: $risk%" else "Không có đánh giá"
                        if (explanation.isNotBlank()) {
                            tvRisk.append(" — $explanation")
                        }
                    }
                }
                conn.disconnect()
            } catch (_: Exception) {
                // ignore network failure for UI-only feature
            } finally {
                runOnUiThread { progress.visibility = View.GONE }
            }
        }
    }

    private fun submitFeedback(label: String, address: String, body: String) {
        progress.visibility = View.VISIBLE
        thread {
            try {
                val feedbackUrl = BuildConfig.API_GATEWAY_BASE_URL.trimEnd('/') + "/v1/feedback"
                val payload = JSONObject()
                payload.put("eventId", UUID.randomUUID().toString())
                val androidId = try {
                    Settings.Secure.getString(contentResolver, Settings.Secure.ANDROID_ID) ?: "unknown"
                } catch (e: Exception) { "unknown" }
                payload.put("userId", androidId)
                payload.put("label", label)
                payload.put("sourceType", "SMS")
                payload.put("timestamp", SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'", Locale.US).format(Date()))
                payload.put("riskScore", JSONObject.NULL)
                val metadata = JSONObject()
                metadata.put("address", address)
                metadata.put("snippet", if (body.length > 256) body.take(256) else body)
                payload.put("metadata", metadata)

                val conn = (URL(feedbackUrl).openConnection() as HttpURLConnection).apply {
                    requestMethod = "POST"
                    setRequestProperty("Content-Type", "application/json; charset=UTF-8")
                    doOutput = true
                    connectTimeout = 5000
                    readTimeout = 5000
                }

                OutputStreamWriter(conn.outputStream, "UTF-8").use { it.write(payload.toString()) }
                val code = conn.responseCode
                if (code in 200..299) {
                    runOnUiThread {
                        Toast.makeText(this, "Gửi feedback: $label", Toast.LENGTH_SHORT).show()
                    }
                } else {
                    runOnUiThread {
                        Toast.makeText(this, "Gửi feedback thất bại (HTTP $code)", Toast.LENGTH_SHORT).show()
                    }
                }
                conn.disconnect()
            } catch (e: Exception) {
                runOnUiThread {
                    Toast.makeText(this, "Lỗi khi gửi feedback: ${e.message}", Toast.LENGTH_SHORT).show()
                }
            } finally {
                runOnUiThread { progress.visibility = View.GONE }
            }
        }
    }
}
