package com.sixseven.antiscam.dialer.ui

import android.Manifest
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.media.AudioAttributes
import android.media.RingtoneManager
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.core.app.Person
import com.sixseven.antiscam.R
import com.sixseven.antiscam.dialer.call.CallUiAction
import com.sixseven.antiscam.dialer.debug.IncomingDebugReporter

object CallNotificationController {

    // Use a versioned channel ID so devices recreate the channel with desired heads-up behavior.
    private const val CHANNEL_ID = "incoming_calls_v4"
    private const val CHANNEL_NAME = "Incoming Calls"
    private const val NOTIFICATION_ID = 2701

    fun showIncomingCall(context: Context, callerLabel: String) {
        createChannel(context)

        val canPostNotifications = canNotify(context)
        val hasFullscreenCapability = canUseFullScreenIntent(context)

        IncomingDebugReporter.report(
            event = "incoming_notification_prepare",
            details = mapOf(
                "callerLabel" to callerLabel,
                "canPostNotifications" to canPostNotifications,
                "hasFullscreenCapability" to hasFullscreenCapability,
                "notificationMode" to "call_style"
            )
        )

        if (!canPostNotifications) {
            IncomingDebugReporter.report(
                event = "incoming_notification_skipped",
                details = mapOf(
                    "reason" to "notifications_blocked",
                    "fallbackLaunched" to false
                )
            )
            return
        }

        val contentIntent = IncomingCallActivity.buildIntent(context)
        val contentPendingIntent = PendingIntent.getActivity(
            context,
            101,
            contentIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val answerIntent = Intent(context, CallActionReceiver::class.java).apply {
            action = CallUiAction.ACTION_ANSWER
        }
        val answerPendingIntent = PendingIntent.getBroadcast(
            context,
            102,
            answerIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val declineIntent = Intent(context, CallActionReceiver::class.java).apply {
            action = CallUiAction.ACTION_DECLINE
        }
        val declinePendingIntent = PendingIntent.getBroadcast(
            context,
            103,
            declineIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val callerPerson = Person.Builder()
            .setName(callerLabel)
            .setImportant(true)
            .build()

        val notification = NotificationCompat.Builder(context, CHANNEL_ID)
            .setSmallIcon(android.R.drawable.sym_call_incoming)
            .setContentTitle(callerLabel)
            .setContentText("Đang gọi đến")
            .setPriority(NotificationCompat.PRIORITY_MAX)
            .setCategory(NotificationCompat.CATEGORY_CALL)
            .setVisibility(NotificationCompat.VISIBILITY_PUBLIC)
            .setDefaults(NotificationCompat.DEFAULT_ALL)
            .setOngoing(true)
            .setAutoCancel(false)
            .setContentIntent(contentPendingIntent)
            .setStyle(
                NotificationCompat.CallStyle.forIncomingCall(
                    callerPerson,
                    declinePendingIntent,
                    answerPendingIntent
                )
            )
            .apply {
                if (hasFullscreenCapability) {
                    setFullScreenIntent(contentPendingIntent, true)
                }
            }
            .build()

        val manager = context.getSystemService(NotificationManager::class.java)
        runCatching {
            manager.notify(NOTIFICATION_ID, notification)
            IncomingDebugReporter.report(
                event = "incoming_notification_posted",
                details = mapOf(
                    "callerLabel" to callerLabel,
                    "hasFullscreenCapability" to hasFullscreenCapability,
                    "notificationMode" to "call_style",
                    "channelId" to CHANNEL_ID
                )
            )
        }.onFailure {
            manager.cancel(NOTIFICATION_ID)
            IncomingDebugReporter.report(
                event = "incoming_notification_failed",
                details = mapOf(
                    "callerLabel" to callerLabel,
                    "error" to (it.message ?: it.javaClass.simpleName),
                    "fallbackLaunched" to false,
                    "channelId" to CHANNEL_ID
                )
            )
        }
    }

    fun cancel(context: Context) {
        val manager = context.getSystemService(NotificationManager::class.java)
        manager.cancel(NOTIFICATION_ID)
    }

    private fun createChannel(context: Context) {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O) {
            return
        }

        val manager = context.getSystemService(NotificationManager::class.java)
        val channel = NotificationChannel(
            CHANNEL_ID,
            CHANNEL_NAME,
            NotificationManager.IMPORTANCE_HIGH
        )
        channel.description = "Incoming call floating alerts with accept and decline actions"
        channel.lockscreenVisibility = NotificationCompat.VISIBILITY_PUBLIC
        channel.enableVibration(true)
        channel.setSound(
            RingtoneManager.getDefaultUri(RingtoneManager.TYPE_RINGTONE),
            AudioAttributes.Builder()
                .setUsage(AudioAttributes.USAGE_NOTIFICATION_RINGTONE)
                .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
                .build()
        )
        manager.createNotificationChannel(channel)
    }

    private fun canNotify(context: Context): Boolean {
        val managerCompat = NotificationManagerCompat.from(context)
        if (!managerCompat.areNotificationsEnabled()) {
            return false
        }

        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.TIRAMISU) {
            return true
        }

        return context.checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) ==
            PackageManager.PERMISSION_GRANTED
    }

    private fun canUseFullScreenIntent(context: Context): Boolean {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.UPSIDE_DOWN_CAKE) {
            return true
        }

        val manager = context.getSystemService(NotificationManager::class.java)
        return runCatching { manager.canUseFullScreenIntent() }
            .getOrDefault(false)
    }
}
