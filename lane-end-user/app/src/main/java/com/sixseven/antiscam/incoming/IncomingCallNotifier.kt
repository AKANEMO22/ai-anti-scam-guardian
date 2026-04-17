package com.sixseven.antiscam.incoming

import android.Manifest
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.core.content.ContextCompat

object IncomingCallNotifier {
    private const val DEFAULT_CALLER_LABEL = "Số đang gọi"

    fun ensureChannel(context: Context) {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O) {
            return
        }

        val manager = context.getSystemService(NotificationManager::class.java) ?: return
        val existingChannel = manager.getNotificationChannel(IncomingCallContracts.CHANNEL_ID)
        if (existingChannel != null) {
            return
        }

        val channel = NotificationChannel(
            IncomingCallContracts.CHANNEL_ID,
            IncomingCallContracts.CHANNEL_NAME,
            NotificationManager.IMPORTANCE_HIGH
        ).apply {
            description = "Alert user with full-screen incoming call UI"
            lockscreenVisibility = android.app.Notification.VISIBILITY_PUBLIC
            setBypassDnd(false)
        }

        manager.createNotificationChannel(channel)
    }

    fun showIncomingCall(context: Context, callerLabel: String) {
        val appContext = context.applicationContext
        ensureChannel(appContext)

        val safeCallerLabel = callerLabel.trim().ifBlank { DEFAULT_CALLER_LABEL }

        val fullScreenIntent = buildIncomingActivityIntent(appContext, safeCallerLabel)
        val fullScreenPendingIntent = PendingIntent.getActivity(
            appContext,
            7001,
            fullScreenIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        launchIncomingUi(appContext, fullScreenIntent)

        if (!canPostNotifications(appContext)) {
            return
        }

        val answerIntent = Intent(appContext, IncomingCallActionReceiver::class.java).apply {
            action = IncomingCallContracts.ACTION_ANSWER
            setPackage(appContext.packageName)
            putExtra(IncomingCallContracts.EXTRA_CALLER_LABEL, safeCallerLabel)
        }
        val answerPendingIntent = PendingIntent.getBroadcast(
            appContext,
            7002,
            answerIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val declineIntent = Intent(appContext, IncomingCallActionReceiver::class.java).apply {
            action = IncomingCallContracts.ACTION_DECLINE
            setPackage(appContext.packageName)
            putExtra(IncomingCallContracts.EXTRA_CALLER_LABEL, safeCallerLabel)
        }
        val declinePendingIntent = PendingIntent.getBroadcast(
            appContext,
            7003,
            declineIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val notification = NotificationCompat.Builder(appContext, IncomingCallContracts.CHANNEL_ID)
            .setSmallIcon(android.R.drawable.sym_call_incoming)
            .setContentTitle("Cuộc gọi đến")
            .setContentText(safeCallerLabel)
            .setCategory(NotificationCompat.CATEGORY_CALL)
            .setPriority(NotificationCompat.PRIORITY_MAX)
            .setVisibility(NotificationCompat.VISIBILITY_PUBLIC)
            .setOngoing(true)
            .setAutoCancel(false)
            .setContentIntent(fullScreenPendingIntent)
            .setFullScreenIntent(fullScreenPendingIntent, true)
            .addAction(android.R.drawable.ic_menu_call, "Trả lời", answerPendingIntent)
            .addAction(android.R.drawable.ic_menu_close_clear_cancel, "Từ chối", declinePendingIntent)
            .build()

        NotificationManagerCompat.from(appContext)
            .notify(IncomingCallContracts.NOTIFICATION_ID, notification)
    }

    fun cancelIncomingCall(context: Context) {
        NotificationManagerCompat.from(context.applicationContext)
            .cancel(IncomingCallContracts.NOTIFICATION_ID)
    }

    private fun canPostNotifications(context: Context): Boolean {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU &&
            ContextCompat.checkSelfPermission(
                context,
                Manifest.permission.POST_NOTIFICATIONS
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            return false
        }

        return NotificationManagerCompat.from(context).areNotificationsEnabled()
    }

    private fun buildIncomingActivityIntent(context: Context, callerLabel: String): Intent {
        return Intent(context, IncomingCallActivity::class.java).apply {
            putExtra(IncomingCallContracts.EXTRA_CALLER_LABEL, callerLabel)
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or
                Intent.FLAG_ACTIVITY_CLEAR_TOP or
                Intent.FLAG_ACTIVITY_SINGLE_TOP
        }
    }

    private fun launchIncomingUi(context: Context, intent: Intent) {
        runCatching { context.startActivity(intent) }
    }
}
