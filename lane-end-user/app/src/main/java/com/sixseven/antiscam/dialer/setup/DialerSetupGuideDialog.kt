package com.sixseven.antiscam.dialer.setup

import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import com.sixseven.antiscam.dialer.role.DefaultDialerRoleHelper

object DialerSetupGuideDialog {

    fun show(activity: AppCompatActivity) {
        val title = "Enable Phone App Mode"
        val message = if (DefaultDialerRoleHelper.isXiaomiFamilyDevice()) {
            "HyperOS/MIUI co the chan quyen nhay cam voi app cai tu file APK.\n\n" +
                "Buoc 1: Mo App info cua Anti-Scam Guardian.\n" +
                "Buoc 2: Bam menu goc phai tren va chon Allow restricted settings.\n" +
                "Buoc 3: Cho phep quyen Phone + Notification cho app.\n" +
                "Buoc 4: Bat Popup/Display over other apps + Full-screen notification.\n" +
                "Buoc 5: Quay lai app, vao Default apps va chon Anti-Scam Guardian lam Phone app."
        } else {
            "Voi ColorOS/OriginOS/OneUI va Android goc, hay cap quyen Phone + Notification, bat Full-screen call popup (neu co), sau do dat Anti-Scam Guardian lam Phone app mac dinh de app hien man hinh nhan cuoc goi den tren cac app khac."
        }

        AlertDialog.Builder(activity)
            .setTitle(title)
            .setMessage(message)
            .setCancelable(true)
            .setPositiveButton("Open Default Apps") { _, _ ->
                val opened = DefaultDialerRoleHelper.openDefaultAppSettings(activity)
                if (!opened) {
                    DefaultDialerRoleHelper.openAppDetailsSettings(activity)
                }
            }
            .setNeutralButton("Open Permission Settings") { _, _ ->
                val opened = DefaultDialerRoleHelper.openPopupPermissionSettings(activity) ||
                    DefaultDialerRoleHelper.openRestrictedPermissionSettings(activity)
                if (!opened) {
                    DefaultDialerRoleHelper.openAppDetailsSettings(activity)
                }
            }
            .setNegativeButton("Later", null)
            .show()
    }
}
