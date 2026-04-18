package com.sixseven.antiscam.service.background

import android.Manifest
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.provider.CallLog
import android.provider.Telephony
import android.util.Log
import androidx.core.content.ContextCompat
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.sixseven.antiscam.core.ml.OnDeviceFilterPipelineResult
import org.json.JSONArray
import org.json.JSONObject
import java.io.File

class BackgroundMonitorWorker(
    context: Context,
    params: WorkerParameters
) : CoroutineWorker(context, params) {

    private val TAG = "BackgroundMonitorWorker"

    fun ingestMobileAppSignal(request: MobileAppToBackgroundServiceRequest): BackgroundServiceDispatchAck {
        // TODO: entrypoint for Mobile App -> Background Service signal handoff.
        throw NotImplementedError("Stub only")
    }

    override suspend fun doWork(): Result {
        try {
            val ctx = applicationContext

            // Files to store cached history for UI to consume
            val callsFile = File(ctx.filesDir, "history_calls.json")
            val smsFile = File(ctx.filesDir, "history_sms.json")

            // Collect recent call log (if permission granted)
            if (ContextCompat.checkSelfPermission(ctx, Manifest.permission.READ_CALL_LOG) == PackageManager.PERMISSION_GRANTED) {
                val callsArray = JSONArray()
                val projection = arrayOf(
                    CallLog.Calls.NUMBER,
                    CallLog.Calls.CACHED_NAME,
                    CallLog.Calls.TYPE,
                    CallLog.Calls.DATE,
                    CallLog.Calls.DURATION
                )

                val cursor = ctx.contentResolver.query(
                    CallLog.Calls.CONTENT_URI,
                    projection,
                    null,
                    null,
                    "${CallLog.Calls.DATE} DESC LIMIT 100"
                )

                cursor?.use { cur ->
                    while (cur.moveToNext()) {
                        val number = cur.getString(0).orEmpty()
                        val cachedName = cur.getString(1).orEmpty()
                        val type = cur.getInt(2)
                        val date = cur.getLong(3)
                        val duration = cur.getLong(4)

                        val obj = JSONObject()
                        obj.put("number", number)
                        obj.put("name", cachedName)
                        obj.put("type", type)
                        obj.put("date", date)
                        obj.put("duration", duration)
                        callsArray.put(obj)
                    }
                }

                try {
                    callsFile.writeText(callsArray.toString())
                } catch (e: Exception) {
                    Log.w(TAG, "Failed to write calls cache: ${e.message}")
                }
            }

            // Collect recent SMS (if permission granted)
            if (ContextCompat.checkSelfPermission(ctx, Manifest.permission.READ_SMS) == PackageManager.PERMISSION_GRANTED) {
                val smsArray = JSONArray()
                val projectionSms = arrayOf(
                    Telephony.Sms.ADDRESS,
                    Telephony.Sms.BODY,
                    Telephony.Sms.DATE,
                    Telephony.Sms.TYPE
                )

                val cursorSms = ctx.contentResolver.query(
                    Telephony.Sms.CONTENT_URI,
                    projectionSms,
                    null,
                    null,
                    "${Telephony.Sms.DATE} DESC LIMIT 100"
                )

                cursorSms?.use { cur ->
                    while (cur.moveToNext()) {
                        val address = cur.getString(0).orEmpty()
                        val body = cur.getString(1).orEmpty()
                        val date = cur.getLong(2)
                        val type = cur.getInt(3)

                        val obj = JSONObject()
                        obj.put("address", address)
                        obj.put("body", body)
                        obj.put("date", date)
                        obj.put("type", type)
                        smsArray.put(obj)
                    }
                }

                try {
                    smsFile.writeText(smsArray.toString())
                } catch (e: Exception) {
                    Log.w(TAG, "Failed to write sms cache: ${e.message}")
                }
            }

            // Notify any running UI to refresh
            try {
                val intent = Intent("com.sixseven.antiscam.ACTION_HISTORY_UPDATED")
                ctx.sendBroadcast(intent)
            } catch (_: Exception) { /* ignore */ }

            return Result.success()
        } catch (e: Exception) {
            Log.e(TAG, "Background monitor failed", e)
            return Result.failure()
        }
    }
}
