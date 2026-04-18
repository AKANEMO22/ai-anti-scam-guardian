package com.sixseven.antiscam.dialer.permissions

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.os.Build

object CallPermissionManager {

    fun requiredPermissions(): Array<String> {
        val permissions = mutableListOf(
            Manifest.permission.READ_PHONE_STATE,
            Manifest.permission.ANSWER_PHONE_CALLS
        )

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            permissions += Manifest.permission.POST_NOTIFICATIONS
        }

        return permissions.toTypedArray()
    }

    fun hasAllPermissions(context: Context): Boolean {
        return requiredPermissions().all { permission ->
            context.checkSelfPermission(permission) == PackageManager.PERMISSION_GRANTED
        }
    }
}
