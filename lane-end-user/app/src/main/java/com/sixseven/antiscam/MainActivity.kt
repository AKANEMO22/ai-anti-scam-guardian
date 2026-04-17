package com.sixseven.antiscam

import android.Manifest
import android.app.role.RoleManager
import android.animation.ObjectAnimator
import android.animation.ValueAnimator
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Color
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.provider.CallLog
import android.provider.ContactsContract
import android.provider.Telephony
import android.provider.Settings
import android.telecom.TelecomManager
import android.view.MotionEvent
import android.view.View
import android.view.ViewGroup
import androidx.appcompat.app.AlertDialog
import org.json.JSONObject
import java.io.BufferedReader
import java.io.InputStreamReader
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URL
import java.util.UUID
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast
import android.view.animation.AccelerateDecelerateInterpolator
import android.view.animation.OvershootInterpolator
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.updatePadding
import com.sixseven.antiscam.incoming.IncomingCallNotifier
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class MainActivity : AppCompatActivity() {

    private lateinit var tabs: List<TextView>
    private lateinit var contentScroll: ScrollView
    private lateinit var tabSections: Map<Int, List<View>>
    private lateinit var callSetupStatusView: TextView
    private lateinit var callSetupHintView: TextView
    private lateinit var shieldPillView: TextView
    private lateinit var callHistoryStatusView: TextView
    private lateinit var callHistoryContainer: LinearLayout
    private lateinit var smsStatusView: TextView
    private lateinit var smsContainer: LinearLayout
    private var activeTabId: Int = R.id.tabHome

    private val contactNameCache = mutableMapOf<String, String>()

    private data class CallHistoryEntry(
        val displayName: String,
        val number: String,
        val type: Int,
        val timestampMs: Long,
        val durationSec: Long
    )

    private data class SmsEntry(
        val address: String,
        val bodyPreview: String,
        val bodyFull: String,
        val timestampMs: Long,
        val type: Int
    )

    private val callPermissionLauncher =
        registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { grantMap ->
            val denied = grantMap.filterValues { granted -> !granted }.keys
            if (denied.isEmpty()) {
                completeIncomingCallSetup()
            } else {
                val permanentlyDenied = denied.filter { permission ->
                    !shouldShowRequestPermissionRationale(permission)
                }

                if (permanentlyDenied.isNotEmpty()) {
                    Toast.makeText(this, "Quyền đã bị từ chối vĩnh viễn. Mở App Settings để bật lại.", Toast.LENGTH_LONG).show()
                    openAppSettings()
                    renderCallSetupStatus()
                    return@registerForActivityResult
                }

                Toast.makeText(this, "Thiếu quyền cho cuộc gọi và messaging", Toast.LENGTH_LONG).show()
            }

            renderCallSetupStatus()
        }

    private val defaultDialerRoleLauncher =
        registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { _ ->
            if (isDefaultDialerApp()) {
                Toast.makeText(this, "Đã đặt app làm Phone mặc định", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "Cần đặt app làm Phone mặc định để xử lý cuộc gọi", Toast.LENGTH_LONG).show()
            }

            renderCallSetupStatus()
        }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        bindCallSetupPanel()
        applySystemInsets()
        setupSections()
        runEntryAnimation()
        runShieldPulseAnimation()
        runCardStaggerAnimation()
        setupTabs()
        attachPressScaleAnimation()
        renderCallSetupStatus()
        renderCallHistory()
    }

    override fun onResume() {
        super.onResume()
        renderCallSetupStatus()
        renderCallHistory()
        if (activeTabId == R.id.tabScan) {
            renderMessagingInbox()
        }
    }

    private fun applySystemInsets() {
        val phoneFrame = findViewById<View>(R.id.phoneFrame)
        val baseTopPadding = phoneFrame.paddingTop

        ViewCompat.setOnApplyWindowInsetsListener(phoneFrame) { view, insets ->
            val topInset = insets.getInsets(WindowInsetsCompat.Type.statusBars()).top
            view.updatePadding(top = baseTopPadding + topInset)
            insets
        }

        ViewCompat.requestApplyInsets(phoneFrame)
    }

    private fun runEntryAnimation() {
        val phoneFrame = findViewById<View>(R.id.phoneFrame)
        phoneFrame.alpha = 0f
        phoneFrame.translationY = 56f
        phoneFrame.animate()
            .alpha(1f)
            .translationY(0f)
            .setDuration(760)
            .setInterpolator(OvershootInterpolator(0.78f))
            .start()
    }

    private fun runShieldPulseAnimation() {
        val shield = findViewById<View>(R.id.shieldPill)

        ObjectAnimator.ofFloat(shield, View.ALPHA, 1f, 0.7f, 1f).apply {
            duration = 1100L
            repeatCount = ValueAnimator.INFINITE
            repeatMode = ValueAnimator.RESTART
            interpolator = AccelerateDecelerateInterpolator()
            start()
        }

        ObjectAnimator.ofFloat(shield, View.SCALE_X, 1f, 1.03f, 1f).apply {
            duration = 1100L
            repeatCount = ValueAnimator.INFINITE
            repeatMode = ValueAnimator.RESTART
            interpolator = AccelerateDecelerateInterpolator()
            start()
        }

        ObjectAnimator.ofFloat(shield, View.SCALE_Y, 1f, 1.03f, 1f).apply {
            duration = 1100L
            repeatCount = ValueAnimator.INFINITE
            repeatMode = ValueAnimator.RESTART
            interpolator = AccelerateDecelerateInterpolator()
            start()
        }
    }

    private fun runCardStaggerAnimation() {
        val cardIds = listOf(
            R.id.cardCallSetup,
            R.id.cardRisk,
            R.id.cardSnapshot,
            R.id.cardAlert,
            R.id.tabBar
        )

        cardIds.forEachIndexed { index, id ->
            val view = findViewById<View>(id)
            view.alpha = 0f
            view.translationY = 24f
            view.animate()
                .alpha(1f)
                .translationY(0f)
                .setStartDelay((index * 95).toLong())
                .setDuration(320)
                .setInterpolator(AccelerateDecelerateInterpolator())
                .start()
        }
    }

    private fun attachPressScaleAnimation() {
        attachPressScale(
            findViewById(R.id.btnCallSetupPrimary),
            findViewById(R.id.tabHome),
            findViewById(R.id.tabScan),
            findViewById(R.id.tabHistory),
            findViewById(R.id.tabGuardian),
            findViewById(R.id.tabSettings)
        )
    }

    private fun setupTabs() {
        tabs = listOf(
            findViewById(R.id.tabHome),
            findViewById(R.id.tabScan),
            findViewById(R.id.tabHistory),
            findViewById(R.id.tabGuardian),
            findViewById(R.id.tabSettings)
        )

        tabs.forEach { tab ->
            tab.setOnClickListener { setActiveTab(tab) }
        }

        findViewById<View>(R.id.btnCallSetupPrimary).setOnClickListener { requestIncomingCallSetup() }

        setActiveTab(findViewById(R.id.tabHome))
    }

    private fun setupSections() {
        contentScroll = findViewById(R.id.scrollContent)

        val homeViews = listOf(
            findViewById<View>(R.id.cardCallSetup),
            findViewById<View>(R.id.cardRisk),
            findViewById<View>(R.id.cardSnapshot),
            findViewById<View>(R.id.cardAlert)
        )

        tabSections = mapOf(
            R.id.tabHome to homeViews,
            R.id.tabScan to listOf(findViewById<View>(R.id.sectionScan)),
            R.id.tabHistory to listOf(findViewById<View>(R.id.sectionHistory)),
            R.id.tabGuardian to listOf(findViewById<View>(R.id.sectionGuardian)),
            R.id.tabSettings to listOf(findViewById<View>(R.id.sectionSettings))
        )
    }

    private fun setActiveTab(active: TextView) {
        activeTabId = active.id

        tabs.forEach { tab ->
            val isActive = tab.id == active.id
            tab.setBackgroundResource(if (isActive) R.drawable.bg_tab_active else R.drawable.bg_tab_inactive)
            tab.setTextColor(Color.parseColor(if (isActive) "#115e59" else "#475569"))
        }

        val activeViews = tabSections[active.id].orEmpty().toSet()
        tabSections.values.flatten().distinct().forEach { sectionView ->
            sectionView.visibility = if (activeViews.contains(sectionView)) View.VISIBLE else View.GONE
        }

        activeViews.forEach { sectionView ->
            sectionView.alpha = 0f
            sectionView.animate()
                .alpha(1f)
                .setDuration(180)
                .setInterpolator(AccelerateDecelerateInterpolator())
                .start()
        }

        contentScroll.post { contentScroll.smoothScrollTo(0, 0) }

        if (active.id == R.id.tabHome) {
            renderCallHistory()
        } else if (active.id == R.id.tabScan) {
            renderMessagingInbox()
        }
    }

    private fun requestIncomingCallSetup() {
        val missing = missingCallPermissions()

        if (missing.isEmpty()) {
            completeIncomingCallSetup()
            return
        }

        callPermissionLauncher.launch(missing.toTypedArray())
    }

    private fun completeIncomingCallSetup() {
        IncomingCallNotifier.ensureChannel(this)
        requestDefaultDialerRoleIfNeeded()
        if (isDefaultDialerApp()) {
            Toast.makeText(this, "Chế độ nhận cuộc gọi đến đã được bật", Toast.LENGTH_SHORT).show()
        }

        renderCallSetupStatus()
    }

    private fun requestDefaultDialerRoleIfNeeded() {
        if (isDefaultDialerApp()) {
            return
        }

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            val roleManager = getSystemService(RoleManager::class.java)
            if (roleManager != null && roleManager.isRoleAvailable(RoleManager.ROLE_DIALER) && !roleManager.isRoleHeld(RoleManager.ROLE_DIALER)) {
                defaultDialerRoleLauncher.launch(roleManager.createRequestRoleIntent(RoleManager.ROLE_DIALER))
            } else {
                openDefaultAppSettings()
            }
            return
        }

        val requestIntent = Intent(TelecomManager.ACTION_CHANGE_DEFAULT_DIALER).apply {
            putExtra(TelecomManager.EXTRA_CHANGE_DEFAULT_DIALER_PACKAGE_NAME, packageName)
        }
        defaultDialerRoleLauncher.launch(requestIntent)
    }

    private fun isDefaultDialerApp(): Boolean {
        val telecomManager = getSystemService(TelecomManager::class.java) ?: return false
        return telecomManager.defaultDialerPackage == packageName
    }

    private fun openAppSettings() {
        val settingsIntent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS).apply {
            data = Uri.fromParts("package", packageName, null)
        }
        startActivity(settingsIntent)
    }

    private fun openDefaultAppSettings() {
        val settingsIntent = Intent(Settings.ACTION_MANAGE_DEFAULT_APPS_SETTINGS)
        if (settingsIntent.resolveActivity(packageManager) != null) {
            startActivity(settingsIntent)
        } else {
            openAppSettings()
        }
    }

    private fun bindCallSetupPanel() {
        shieldPillView = findViewById(R.id.shieldPill)
        callSetupStatusView = findViewById(R.id.tvCallSetupStatus)
        callSetupHintView = findViewById(R.id.tvCallSetupHint)
        callHistoryStatusView = findViewById(R.id.tvCallHistoryStatus)
        callHistoryContainer = findViewById(R.id.layoutCallHistoryContainer)
        smsStatusView = findViewById(R.id.tvSmsStatus)
        smsContainer = findViewById(R.id.layoutSmsContainer)
    }

    private fun renderCallSetupStatus() {
        val missingPermissions = missingCallPermissions()
        val isDefaultDialer = isDefaultDialerApp()
        val isReady = missingPermissions.isEmpty() && isDefaultDialer
        updateShieldIndicator(isReady)

        if (isReady) {
            callSetupStatusView.text = "Sẵn sàng cuộc gọi và messaging"
            callSetupStatusView.setTextColor(Color.parseColor("#166534"))
            callSetupHintView.text = "Đã cấp đủ quyền cuộc gọi/tin nhắn và đã đặt app làm Phone mặc định."
            findViewById<TextView>(R.id.btnCallSetupPrimary).text = "Kiểm tra lại cấu hình"
            return
        }

        callSetupStatusView.text = "Còn thiếu quyền cấu hình"
        callSetupStatusView.setTextColor(Color.parseColor("#b91c1c"))

        val hintBuilder = StringBuilder()
        if (missingPermissions.isNotEmpty()) {
            hintBuilder.append("Cần cấp quyền: ")
            hintBuilder.append(
                missingPermissions.joinToString(", ") { permission ->
                    permission.substringAfterLast('.')
                }
            )
            hintBuilder.append(". ")
        }

        if (!isDefaultDialer) {
            hintBuilder.append("Cần đặt app làm Phone mặc định để hiện UI cuộc gọi đến.")
        }

        callSetupHintView.text = hintBuilder.toString().trim()
        findViewById<TextView>(R.id.btnCallSetupPrimary).text = "Cấp quyền cuộc gọi và tin nhắn"
    }

    private fun updateShieldIndicator(isReady: Boolean) {
        shieldPillView.text = if (isReady) "SHIELD ACTIVE" else "SHIELD INACTIVE"
        shieldPillView.setTextColor(
            Color.parseColor(
                if (isReady) {
                    "#166534"
                } else {
                    "#b91c1c"
                }
            )
        )
        shieldPillView.setBackgroundResource(
            if (isReady) {
                R.drawable.bg_pill_shield
            } else {
                R.drawable.bg_pill_shield_inactive
            }
        )
    }

    private fun missingCallPermissions(): List<String> {
        val required = mutableListOf(
            Manifest.permission.READ_PHONE_STATE,
            Manifest.permission.ANSWER_PHONE_CALLS,
            Manifest.permission.READ_CALL_LOG,
            Manifest.permission.READ_CONTACTS,
            Manifest.permission.READ_SMS
        )

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            required += Manifest.permission.POST_NOTIFICATIONS
        }

        return required.filter { permission ->
            ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED
        }
    }

    private fun attachPressScale(vararg views: View) {
        views.forEach { view ->
            view.setOnTouchListener { _, event ->
                when (event.actionMasked) {
                    MotionEvent.ACTION_DOWN -> {
                        view.animate().scaleX(0.97f).scaleY(0.97f).setDuration(80).start()
                    }

                    MotionEvent.ACTION_UP,
                    MotionEvent.ACTION_CANCEL -> {
                        view.animate().scaleX(1f).scaleY(1f).setDuration(120).start()
                    }
                }
                false
            }
        }
    }

    private fun renderMessagingInbox() {
        if (!::smsStatusView.isInitialized || !::smsContainer.isInitialized) {
            return
        }

        smsContainer.removeAllViews()

        if (!hasPermission(Manifest.permission.READ_SMS)) {
            smsStatusView.text = "Chưa có quyền READ_SMS. Hãy cấp ở tab Home bằng nút Cấp quyền cuộc gọi và tin nhắn."
            return
        }

        val entries = loadSmsEntries(limit = 30)
        if (entries.isEmpty()) {
            smsStatusView.text = "Không có tin nhắn SMS nào trong máy."
            return
        }

        smsStatusView.text = "Tổng ${entries.size} tin nhắn gần đây."
        entries.forEach { entry ->
            smsContainer.addView(buildSmsRow(entry))
        }
    }

    private fun loadSmsEntries(limit: Int): List<SmsEntry> {
        val entries = mutableListOf<SmsEntry>()
        val projection = arrayOf(
            Telephony.Sms.ADDRESS,
            Telephony.Sms.BODY,
            Telephony.Sms.DATE,
            Telephony.Sms.TYPE
        )

        val cursor = runCatching {
            contentResolver.query(
                Telephony.Sms.CONTENT_URI,
                projection,
                null,
                null,
                "${Telephony.Sms.DATE} DESC"
            )
        }.getOrNull() ?: return entries

        cursor.use {
            while (it.moveToNext() && entries.size < limit) {
                val rawAddress = it.getString(0).orEmpty().trim()
                val address = rawAddress.ifBlank { "Không rõ số" }
                val body = it.getString(1).orEmpty().trim().ifBlank { "(Không có nội dung)" }
                val normalizedBody = body.replace("\n", " ")
                val preview = if (normalizedBody.length > 96) {
                    "${normalizedBody.take(96)}..."
                } else {
                    normalizedBody
                }

                entries += SmsEntry(
                    address = address,
                    bodyPreview = preview,
                    bodyFull = body,
                    timestampMs = it.getLong(2),
                    type = it.getInt(3)
                )
            }
        }

        return entries
    }

    private fun buildSmsRow(entry: SmsEntry): View {
        val row = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundResource(R.drawable.bg_kpi_card)
            setPadding(dp(10), dp(10), dp(10), dp(10))
            layoutParams = LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            ).apply {
                bottomMargin = dp(8)
            }
        }

        val primaryLine = TextView(this).apply {
            text = entry.address
            setTextColor(Color.parseColor("#0f172a"))
            textSize = 13f
            setTypeface(typeface, android.graphics.Typeface.BOLD)
        }

        val secondaryLine = TextView(this).apply {
            text = "${formatSmsType(entry.type)} • ${formatCallDate(entry.timestampMs)}"
            setTextColor(Color.parseColor("#64748b"))
            textSize = 11f
        }

        val messageLine = TextView(this).apply {
            text = entry.bodyPreview
            setTextColor(Color.parseColor("#334155"))
            textSize = 12f
            setPadding(0, dp(4), 0, 0)
        }

        row.addView(primaryLine)
        row.addView(secondaryLine)
        row.addView(messageLine)

        row.isClickable = true
        row.setOnClickListener {
            showSmsDetail(entry)
        }

        return row
    }

    private fun showSmsDetail(entry: SmsEntry) {
        // Open dedicated in-app detail screen for message (UI-only change)
        val intent = Intent(this, com.sixseven.antiscam.warning.WarningDetailActivity::class.java).apply {
            putExtra(com.sixseven.antiscam.warning.WarningDetailActivity.EXTRA_ADDRESS, entry.address)
            putExtra(com.sixseven.antiscam.warning.WarningDetailActivity.EXTRA_BODY, entry.bodyFull)
            putExtra(com.sixseven.antiscam.warning.WarningDetailActivity.EXTRA_TIMESTAMP, entry.timestampMs)
        }
        startActivity(intent)
    }

    private fun submitFeedback(entry: SmsEntry, label: String) {
        Thread {
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
                payload.put("timestamp", java.text.SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'", java.util.Locale.US).format(java.util.Date()))
                payload.put("riskScore", JSONObject.NULL)
                payload.put("metadata", JSONObject())

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
                    val resp = BufferedReader(InputStreamReader(conn.inputStream)).use { it.readText() }
                    val json = JSONObject(resp)
                    val accepted = json.optBoolean("accepted", false)
                    runOnUiThread {
                        Toast.makeText(this, if (accepted) "Gửi feedback thành công" else "Feedback gửi nhưng không được chấp nhận", Toast.LENGTH_SHORT).show()
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
            }
        }.start()
    }

    private fun formatSmsType(type: Int): String {
        return when (type) {
            Telephony.Sms.MESSAGE_TYPE_INBOX -> "Tin nhắn đến"
            Telephony.Sms.MESSAGE_TYPE_SENT -> "Tin nhắn đã gửi"
            Telephony.Sms.MESSAGE_TYPE_DRAFT -> "Tin nhắn nháp"
            Telephony.Sms.MESSAGE_TYPE_OUTBOX -> "Tin nhắn đi"
            Telephony.Sms.MESSAGE_TYPE_FAILED -> "Tin nhắn lỗi"
            Telephony.Sms.MESSAGE_TYPE_QUEUED -> "Tin nhắn chờ gửi"
            else -> "Tin nhắn khác"
        }
    }

    private fun renderCallHistory() {
        if (!::callHistoryStatusView.isInitialized || !::callHistoryContainer.isInitialized) {
            return
        }

        callHistoryContainer.removeAllViews()
        contactNameCache.clear()

        if (!hasPermission(Manifest.permission.READ_CALL_LOG)) {
            callHistoryStatusView.text = "Cần cấp quyền READ_CALL_LOG để hiển thị lịch sử cuộc gọi."
            return
        }

        val entries = loadCallHistoryEntries()
        if (entries.isEmpty()) {
            callHistoryStatusView.text = "Không có lịch sử cuộc gọi."
            return
        }

        callHistoryStatusView.text = "Tổng ${entries.size} cuộc gọi gần đây."
        entries.forEach { entry ->
            callHistoryContainer.addView(buildCallHistoryRow(entry))
        }
    }

    private fun loadCallHistoryEntries(): List<CallHistoryEntry> {
        val entries = mutableListOf<CallHistoryEntry>()
        val projection = arrayOf(
            CallLog.Calls.NUMBER,
            CallLog.Calls.CACHED_NAME,
            CallLog.Calls.TYPE,
            CallLog.Calls.DATE,
            CallLog.Calls.DURATION
        )

        val cursor = runCatching {
            contentResolver.query(
                CallLog.Calls.CONTENT_URI,
                projection,
                null,
                null,
                "${CallLog.Calls.DATE} DESC"
            )
        }.getOrNull() ?: return entries

        cursor.use {
            val canReadContacts = hasPermission(Manifest.permission.READ_CONTACTS)
            while (it.moveToNext()) {
                val rawNumber = it.getString(0).orEmpty().trim()
                val number = rawNumber.ifBlank { "Số riêng tư" }
                val cachedName = it.getString(1).orEmpty().trim()
                val resolvedName = when {
                    cachedName.isNotBlank() -> cachedName
                    canReadContacts && rawNumber.isNotBlank() -> resolveContactName(rawNumber)
                    else -> ""
                }

                entries += CallHistoryEntry(
                    displayName = resolvedName.ifBlank { number },
                    number = number,
                    type = it.getInt(2),
                    timestampMs = it.getLong(3),
                    durationSec = it.getLong(4)
                )
            }
        }

        return entries
    }

    private fun resolveContactName(number: String): String {
        contactNameCache[number]?.let { cached ->
            return cached
        }

        val lookupUri = Uri.withAppendedPath(
            ContactsContract.PhoneLookup.CONTENT_FILTER_URI,
            Uri.encode(number)
        )

        val resolved = runCatching {
            contentResolver.query(
                lookupUri,
                arrayOf(ContactsContract.PhoneLookup.DISPLAY_NAME),
                null,
                null,
                null
            )?.use { cursor ->
                if (cursor.moveToFirst()) cursor.getString(0).orEmpty().trim() else ""
            }.orEmpty()
        }.getOrDefault("")

        contactNameCache[number] = resolved
        return resolved
    }

    private fun buildCallHistoryRow(entry: CallHistoryEntry): View {
        val row = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundResource(R.drawable.bg_kpi_card)
            setPadding(dp(10), dp(10), dp(10), dp(10))
            layoutParams = LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            ).apply {
                bottomMargin = dp(8)
            }
        }

        val primaryLine = TextView(this).apply {
            text = if (entry.displayName == entry.number) {
                entry.number
            } else {
                "${entry.displayName} (${entry.number})"
            }
            setTextColor(Color.parseColor("#0f172a"))
            textSize = 13f
            setTypeface(typeface, android.graphics.Typeface.BOLD)
        }

        val secondaryLine = TextView(this).apply {
            val typeLabel = formatCallType(entry.type)
            val dateLabel = formatCallDate(entry.timestampMs)
            val durationLabel = formatCallDuration(entry.type, entry.durationSec)
            text = "$typeLabel • $dateLabel • $durationLabel"
            setTextColor(Color.parseColor("#64748b"))
            textSize = 11f
        }

        row.addView(primaryLine)
        row.addView(secondaryLine)
        return row
    }

    private fun formatCallType(type: Int): String {
        return when (type) {
            CallLog.Calls.INCOMING_TYPE -> "Cuộc gọi đến"
            CallLog.Calls.OUTGOING_TYPE -> "Cuộc gọi đi"
            CallLog.Calls.MISSED_TYPE -> "Cuộc gọi nhỡ"
            CallLog.Calls.REJECTED_TYPE -> "Cuộc gọi bị từ chối"
            CallLog.Calls.BLOCKED_TYPE -> "Cuộc gọi bị chặn"
            CallLog.Calls.VOICEMAIL_TYPE -> "Thư thoại"
            else -> "Loại khác"
        }
    }

    private fun formatCallDate(timestampMs: Long): String {
        val formatter = SimpleDateFormat("dd/MM/yyyy HH:mm", Locale("vi", "VN"))
        return formatter.format(Date(timestampMs))
    }

    private fun formatCallDuration(type: Int, durationSec: Long): String {
        if (type == CallLog.Calls.MISSED_TYPE || type == CallLog.Calls.REJECTED_TYPE) {
            return "0 giây"
        }

        val safeDuration = durationSec.coerceAtLeast(0)
        val minutes = safeDuration / 60
        val seconds = safeDuration % 60
        return if (minutes > 0) {
            "$minutes phút $seconds giây"
        } else {
            "$seconds giây"
        }
    }

    private fun hasPermission(permission: String): Boolean {
        return ContextCompat.checkSelfPermission(this, permission) == PackageManager.PERMISSION_GRANTED
    }

    private fun dp(value: Int): Int {
        return (value * resources.displayMetrics.density).toInt()
    }
}
