package com.sixseven.antiscam.dialer.role

import android.app.Activity
import android.app.role.RoleManager
import android.content.ActivityNotFoundException
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Build
import android.provider.Settings
import android.telecom.TelecomManager
import java.util.Locale

object DefaultDialerRoleHelper {

    private const val XIAOMI_SETTINGS = "com.android.settings"
    private const val OPPO_SETTINGS = "com.coloros.safecenter"
    private const val VIVO_SETTINGS = "com.iqoo.secure"
    private const val HUAWEI_SETTINGS = "com.huawei.systemmanager"

    fun isXiaomiFamilyDevice(): Boolean {
        val manufacturer = Build.MANUFACTURER.lowercase(Locale.US)
        val brand = Build.BRAND.lowercase(Locale.US)
        return manufacturer.contains("xiaomi") ||
            brand.contains("xiaomi") ||
            brand.contains("redmi") ||
            brand.contains("poco")
    }

    private fun isSamsungFamilyDevice(): Boolean {
        val manufacturer = Build.MANUFACTURER.lowercase(Locale.US)
        val brand = Build.BRAND.lowercase(Locale.US)
        return manufacturer.contains("samsung") || brand.contains("samsung")
    }

    private fun isOppoFamilyDevice(): Boolean {
        val manufacturer = Build.MANUFACTURER.lowercase(Locale.US)
        val brand = Build.BRAND.lowercase(Locale.US)
        return manufacturer.contains("oppo") ||
            manufacturer.contains("oneplus") ||
            manufacturer.contains("realme") ||
            brand.contains("oppo") ||
            brand.contains("oneplus") ||
            brand.contains("realme")
    }

    private fun isVivoFamilyDevice(): Boolean {
        val manufacturer = Build.MANUFACTURER.lowercase(Locale.US)
        val brand = Build.BRAND.lowercase(Locale.US)
        return manufacturer.contains("vivo") ||
            manufacturer.contains("iqoo") ||
            brand.contains("vivo") ||
            brand.contains("iqoo")
    }

    private fun isHuaweiFamilyDevice(): Boolean {
        val manufacturer = Build.MANUFACTURER.lowercase(Locale.US)
        val brand = Build.BRAND.lowercase(Locale.US)
        return manufacturer.contains("huawei") || brand.contains("huawei")
    }

    fun isDefaultDialer(context: Context): Boolean {
        val telecomManager = context.getSystemService(TelecomManager::class.java)
        return telecomManager?.defaultDialerPackage == context.packageName
    }

    fun buildRoleRequestIntent(context: Context): Intent? {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            val roleManager = context.getSystemService(RoleManager::class.java)
            if (roleManager != null &&
                roleManager.isRoleAvailable(RoleManager.ROLE_DIALER) &&
                !roleManager.isRoleHeld(RoleManager.ROLE_DIALER)
            ) {
                return roleManager.createRequestRoleIntent(RoleManager.ROLE_DIALER)
            }
        }

        val legacyIntent = Intent(TelecomManager.ACTION_CHANGE_DEFAULT_DIALER).apply {
            putExtra(TelecomManager.EXTRA_CHANGE_DEFAULT_DIALER_PACKAGE_NAME, context.packageName)
        }

        return legacyIntent.takeIf {
            legacyIntent.resolveActivity(context.packageManager) != null
        }
    }

    fun openDefaultAppSettings(activity: Activity): Boolean {
        val candidates = mutableListOf<Intent>()

        buildRoleRequestIntent(activity)?.let { candidates += it }
        candidates += Intent(TelecomManager.ACTION_CHANGE_DEFAULT_DIALER).apply {
            putExtra(TelecomManager.EXTRA_CHANGE_DEFAULT_DIALER_PACKAGE_NAME, activity.packageName)
        }

        if (isXiaomiFamilyDevice()) {
            candidates += Intent().setClassName(
                XIAOMI_SETTINGS,
                "com.android.settings.Settings\$ManageDefaultAppsSettingsActivity"
            )
            candidates += Intent().setClassName(
                XIAOMI_SETTINGS,
                "com.android.settings.Settings\$DefaultAppsSettingsActivity"
            )
        }

        if (isSamsungFamilyDevice()) {
            candidates += Intent().setClassName(
                "com.android.settings",
                "com.android.settings.Settings\$DefaultAppsSettingsActivity"
            )
        }

        if (isOppoFamilyDevice()) {
            candidates += Intent().setClassName(
                OPPO_SETTINGS,
                "com.coloros.safecenter.permission.PermissionManagerActivity"
            )
        }

        if (isVivoFamilyDevice()) {
            candidates += Intent().setClassName(
                VIVO_SETTINGS,
                "com.iqoo.secure.MainActivity"
            )
        }

        if (isHuaweiFamilyDevice()) {
            candidates += Intent().setClassName(
                HUAWEI_SETTINGS,
                "com.huawei.permissionmanager.ui.MainActivity"
            )
        }

        candidates += Intent(Settings.ACTION_MANAGE_DEFAULT_APPS_SETTINGS)
        candidates += Intent(Settings.ACTION_APPLICATION_SETTINGS)
        candidates += buildAppDetailsIntent(activity)

        return launchFirstResolvable(activity, candidates)
    }

    fun openRestrictedPermissionSettings(activity: Activity): Boolean {
        val candidates = mutableListOf<Intent>()

        if (isXiaomiFamilyDevice()) {
            candidates += Intent("miui.intent.action.APP_PERM_EDITOR").apply {
                setClassName(
                    "com.miui.securitycenter",
                    "com.miui.permcenter.permissions.PermissionsEditorActivity"
                )
                putExtra("extra_pkgname", activity.packageName)
            }

            candidates += Intent("miui.intent.action.APP_PERM_EDITOR").apply {
                setClassName(
                    "com.miui.securitycenter",
                    "com.miui.permcenter.permissions.AppPermissionsEditorActivity"
                )
                putExtra("extra_pkgname", activity.packageName)
            }
        }

        candidates += buildAppDetailsIntent(activity)
        return launchFirstResolvable(activity, candidates)
    }

    fun openPopupPermissionSettings(activity: Activity): Boolean {
        val candidates = mutableListOf<Intent>()

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.UPSIDE_DOWN_CAKE) {
            candidates += Intent(Settings.ACTION_MANAGE_APP_USE_FULL_SCREEN_INTENT).apply {
                data = Uri.fromParts("package", activity.packageName, null)
            }
        }

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            candidates += Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION).apply {
                data = Uri.fromParts("package", activity.packageName, null)
            }
        }

        if (isXiaomiFamilyDevice()) {
            candidates += Intent("miui.intent.action.APP_PERM_EDITOR").apply {
                setClassName(
                    "com.miui.securitycenter",
                    "com.miui.permcenter.permissions.PermissionsEditorActivity"
                )
                putExtra("extra_pkgname", activity.packageName)
            }
        }

        candidates += buildAppDetailsIntent(activity)
        return launchFirstResolvable(activity, candidates)
    }

    fun openAppDetailsSettings(activity: Activity): Boolean {
        return tryStartActivity(activity, buildAppDetailsIntent(activity))
    }

    private fun buildAppDetailsIntent(activity: Activity): Intent {
        return Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS).apply {
            data = Uri.fromParts("package", activity.packageName, null)
        }
    }

    private fun launchFirstResolvable(activity: Activity, candidates: List<Intent>): Boolean {
        candidates.forEach { candidate ->
            val canResolve = candidate.resolveActivity(activity.packageManager) != null ||
                candidate.component != null
            if (canResolve && tryStartActivity(activity, candidate)) {
                return true
            }
        }

        return tryStartActivity(activity, buildAppDetailsIntent(activity))
    }

    private fun tryStartActivity(activity: Activity, intent: Intent): Boolean {
        return try {
            activity.startActivity(intent)
            true
        } catch (_: ActivityNotFoundException) {
            false
        } catch (_: SecurityException) {
            false
        }
    }
}
