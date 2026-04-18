package com.sixseven.antiscam.incoming

import android.Manifest
import android.app.AlertDialog
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.graphics.BitmapFactory
import android.graphics.Color
import android.media.AudioManager
import android.media.MediaRecorder
import android.net.Uri
import android.os.Build
import android.os.Bundle
// Speech recognition is handled by TranscriptionManager in the InCall service; activity listens for broadcasts
import android.os.Environment
import android.os.SystemClock
import android.os.Handler
import android.os.Looper
import android.provider.ContactsContract
import android.provider.Settings
import android.telecom.Call
import android.telephony.TelephonyManager
import android.view.View
import android.view.WindowManager
import android.widget.Button
import android.widget.Chronometer
import android.widget.EditText
import android.widget.ImageButton
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
// Permission requests are centralized in MainActivity's Call Setup panel
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.sixseven.antiscam.R
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class IncomingCallActivity : AppCompatActivity() {

    private lateinit var callerAvatarView: ImageView
    private lateinit var callerLabelView: TextView
    private lateinit var callMetaView: TextView
    private lateinit var callStateView: TextView
    private lateinit var protectionHintView: TextView
    private lateinit var durationView: Chronometer
    private lateinit var actionStatusView: TextView
    private lateinit var audioCaptureStatusView: TextView
    private lateinit var transcriptView: TextView
    private lateinit var incomingActionsLayout: View
    private lateinit var inCallControlsLayout: View
    private lateinit var bottomControlsLayout: View
    private lateinit var declineLabelView: TextView
    private lateinit var speakerLabelView: TextView
    private lateinit var muteLabelView: TextView
    private lateinit var holdLabelView: TextView
    private lateinit var recordLabelView: TextView
    private lateinit var answerButton: Button
    private lateinit var incomingDeclineButton: Button
    private lateinit var declineButton: ImageButton
    private lateinit var holdButton: ImageButton
    private lateinit var speakerButton: ImageButton
    private lateinit var muteButton: ImageButton
    private lateinit var recordButton: ImageButton
    private lateinit var contactButton: ImageButton
    private lateinit var noteButton: ImageButton

    private var inCallMode = false
    private var timerStarted = false
    private var isSpeakerOn = false
    private var isMicMuted = false
    private var isOnHold = false
    private var isRecording = false
    private var recorder: MediaRecorder? = null
    private var recordingFile: File? = null

    // UI debounce for audio-capture status to avoid rapid flicker
    private val uiHandler = Handler(Looper.getMainLooper())
    private var lastAudioStatusChangeTs = 0L
    private var pendingAudioUiRunnable: Runnable? = null
    private val AUDIO_UI_MIN_INTERVAL = 500L

    // prevent repeatedly opening Call Setup when mic permission missing
    private var microPermissionRequested = false

    // no transcription UI in incoming activity (handled by service)

    private val audioManager by lazy { getSystemService(AudioManager::class.java) }

    // Recording permission is requested centrally in MainActivity; activity will redirect user there when needed.

    // activity will not request RECORD_AUDIO for service-side STT; incoming UI does not display script

    private val callStateReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context, intent: Intent?) {
            val state = intent?.getStringExtra(IncomingCallContracts.EXTRA_CALL_STATE) ?: return
            when (state) {
                TelephonyManager.EXTRA_STATE_RINGING -> {
                    updateCallerFromIntent(intent)
                    showRingingUi()
                }

                TelephonyManager.EXTRA_STATE_OFFHOOK -> {
                    updateCallerFromIntent(intent)
                    showConnectedUi()
                    IncomingCallNotifier.cancelIncomingCall(this@IncomingCallActivity)
                }

                TelephonyManager.EXTRA_STATE_IDLE -> {
                    IncomingCallStateStore.clear()
                    stopDurationTimer(reset = true)
                    stopRecordingIfNeeded()
                    callStateView.text = "Cuộc gọi đã kết thúc"
                    protectionHintView.text = "Đang đóng màn hình cuộc gọi..."
                    showActionStatus("Đã kết thúc cuộc gọi")
                    // clear any shown transcript when call ends
                    runCatching { transcriptView.text = "" }
                    finishSafelyDelayed()
                }

                IncomingCallContracts.STATE_ANSWER_FAILED -> {
                    showActionStatus("Không thể trả lời. Kiểm tra quyền và Phone role.")
                    Toast.makeText(
                        this@IncomingCallActivity,
                        "Không thể trả lời. Kiểm tra quyền ANSWER_PHONE_CALLS",
                        Toast.LENGTH_LONG
                    ).show()
                }

                IncomingCallContracts.STATE_DECLINE_FAILED -> {
                    showActionStatus("Không thể từ chối trên thiết bị này.")
                    Toast.makeText(
                        this@IncomingCallActivity,
                        "Không thể từ chối cuộc gọi trên thiết bị này",
                        Toast.LENGTH_LONG
                    ).show()
                }
            }
        }
    }

    private val transcriptionReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context, intent: Intent?) {
            val action = intent?.action ?: return
            when (action) {
                IncomingCallContracts.ACTION_TRANSCRIPTION_STATUS -> {
                    val capturing = intent.getBooleanExtra(IncomingCallContracts.EXTRA_TRANSCRIPTION_CAPTURING, false)
                    val msg = intent.getStringExtra(IncomingCallContracts.EXTRA_TRANSCRIPTION_STATUS_MESSAGE)
                        updateAudioCaptureUi(capturing, msg)
                }

                IncomingCallContracts.ACTION_TRANSCRIPTION_ERROR -> {
                    val msg = intent.getStringExtra(IncomingCallContracts.EXTRA_TRANSCRIPTION_ERROR)
                        updateAudioCaptureUi(false, msg)
                }

                IncomingCallContracts.ACTION_TRANSCRIPTION_UPDATED -> {
                    val text = intent.getStringExtra(IncomingCallContracts.EXTRA_TRANSCRIPT_TEXT).orEmpty()
                    updateAudioCaptureUi(true, null)
                    if (text.isNotBlank()) {
                        // show the latest transcript (partial or final)
                        runCatching { transcriptView.text = text }
                    }
                }
            }
        }
    }

    private fun registerTranscriptionReceiver() {
        val filter = IntentFilter().apply {
            addAction(IncomingCallContracts.ACTION_TRANSCRIPTION_STATUS)
            addAction(IncomingCallContracts.ACTION_TRANSCRIPTION_ERROR)
            addAction(IncomingCallContracts.ACTION_TRANSCRIPTION_UPDATED)
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            registerReceiver(transcriptionReceiver, filter, Context.RECEIVER_NOT_EXPORTED)
        } else {
            registerReceiver(transcriptionReceiver, filter)
        }
    }

    private fun updateAudioCaptureUi(capturing: Boolean, message: String?) {
        val now = SystemClock.elapsedRealtime()
        val apply = Runnable {
            if (capturing) {
                audioCaptureStatusView.text = "Micro: Đang bắt âm thanh"
                audioCaptureStatusView.setTextColor(Color.parseColor("#22c55e"))
            } else {
                val display = if (!message.isNullOrBlank()) "Micro: Bị chặn — ${message}" else "Micro: Không ghi nhận"
                audioCaptureStatusView.text = display
                audioCaptureStatusView.setTextColor(Color.parseColor("#ef4444"))
                // If message indicates missing RECORD_AUDIO permission, open centralized Call Setup once
                if (!message.isNullOrBlank() && message.contains("RECORD_AUDIO", ignoreCase = true) && !microPermissionRequested) {
                    microPermissionRequested = true
                    // open Call Setup after short delay so UI update is visible
                    uiHandler.postDelayed({ openMainCallSetup() }, 300L)
                }
            }
            lastAudioStatusChangeTs = SystemClock.elapsedRealtime()
            pendingAudioUiRunnable = null
        }

        val delta = now - lastAudioStatusChangeTs
        if (delta < AUDIO_UI_MIN_INTERVAL) {
            pendingAudioUiRunnable?.let { uiHandler.removeCallbacks(it) }
            val r = Runnable { apply.run() }
            pendingAudioUiRunnable = r
            uiHandler.postDelayed(r, AUDIO_UI_MIN_INTERVAL - delta)
        } else {
            apply.run()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableLockScreenMode()
        setContentView(R.layout.activity_incoming_call_v2)

        callerAvatarView = findViewById(R.id.ivCallerAvatar)
        callerLabelView = findViewById(R.id.tvCallerLabel)
        callMetaView = findViewById(R.id.tvCallMeta)
        callStateView = findViewById(R.id.tvCallState)
        protectionHintView = findViewById(R.id.tvProtectionHint)
        durationView = findViewById(R.id.chronometerCallDuration)
        actionStatusView = findViewById(R.id.tvInCallActionStatus)
        audioCaptureStatusView = findViewById(R.id.tvAudioCaptureStatus)
        audioCaptureStatusView.setOnClickListener {
            // Open app settings so user can allow microphone / special permissions (MIUI etc.)
            val settingsIntent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS).apply {
                data = Uri.fromParts("package", packageName, null)
            }
            startActivity(settingsIntent)
        }
        transcriptView = findViewById(R.id.tvTranscript)
        incomingActionsLayout = findViewById(R.id.layoutIncomingActions)
        inCallControlsLayout = findViewById(R.id.layoutInCallControls)
        bottomControlsLayout = findViewById(R.id.layoutBottomControls)
        declineLabelView = findViewById(R.id.tvDeclineLabel)
        speakerLabelView = findViewById(R.id.tvSpeakerLabel)
        muteLabelView = findViewById(R.id.tvMuteLabel)
        holdLabelView = findViewById(R.id.tvHoldLabel)
        recordLabelView = findViewById(R.id.tvRecordLabel)
        answerButton = findViewById(R.id.btnAnswer)
        incomingDeclineButton = findViewById(R.id.btnDeclineIncoming)
        declineButton = findViewById(R.id.btnDecline)
        holdButton = findViewById(R.id.btnHold)
        speakerButton = findViewById(R.id.btnSpeaker)
        muteButton = findViewById(R.id.btnMute)
        recordButton = findViewById(R.id.btnRecord)
        contactButton = findViewById(R.id.btnContact)
        noteButton = findViewById(R.id.btnNote)
        // transcription view removed from layout

        updateCallerFromIntent(intent)
        applyInitialStateFromIntent(intent)
        setupActions()
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        setIntent(intent)
        updateCallerFromIntent(intent)
        applyInitialStateFromIntent(intent)
    }

    override fun onStart() {
        super.onStart()
        registerCallStateReceiver()
        registerTranscriptionReceiver()
        microPermissionRequested = false
    }

    override fun onStop() {
        super.onStop()
        runCatching { unregisterReceiver(callStateReceiver) }
        runCatching { unregisterReceiver(transcriptionReceiver) }
    }

    override fun onDestroy() {
        stopRecordingIfNeeded()
        resetAudioRouteIfNeeded()
        super.onDestroy()
    }

    private fun setupActions() {
        answerButton.setOnClickListener {
            if (inCallMode) {
                return@setOnClickListener
            }

            val answered = IncomingCallControl.answer(this)
            if (answered) {
                showConnectedUi()
                IncomingCallNotifier.cancelIncomingCall(this)
                showActionStatus("Đã trả lời cuộc gọi")
                return@setOnClickListener
            }

            showActionStatus("Không thể trả lời. Kiểm tra quyền và Phone role.")
            Toast.makeText(
                this,
                "Không thể trả lời. Kiểm tra quyền ANSWER_PHONE_CALLS",
                Toast.LENGTH_LONG
            ).show()
        }

        incomingDeclineButton.setOnClickListener { handleDeclineAction() }
        declineButton.setOnClickListener { handleDeclineAction() }

        holdButton.setOnClickListener { toggleHoldState() }
        speakerButton.setOnClickListener { toggleSpeakerState() }
        muteButton.setOnClickListener { toggleMuteState() }
        recordButton.setOnClickListener { toggleRecordingState() }
        contactButton.setOnClickListener { openContactAction() }
        noteButton.setOnClickListener { openNoteEditor() }
    }

    private fun openContactAction() {
        val callerRaw = callerLabelView.text?.toString().orEmpty().trim()
        val callerPhone = extractPhoneNumber(callerRaw)
        val intent = if (callerPhone.isNotBlank()) {
            Intent(Intent.ACTION_INSERT_OR_EDIT).apply {
                type = ContactsContract.Contacts.CONTENT_ITEM_TYPE
                putExtra(ContactsContract.Intents.Insert.PHONE, callerPhone)
                if (callerRaw.isNotBlank() && callerRaw != callerPhone) {
                    putExtra(ContactsContract.Intents.Insert.NAME, callerRaw)
                }
            }
        } else {
            Intent(Intent.ACTION_VIEW, ContactsContract.Contacts.CONTENT_URI)
        }

        if (launchIntentSafely(intent)) {
            showActionStatus(if (callerPhone.isNotBlank()) "Đang mở lưu liên hệ" else "Đang mở danh bạ")
            return
        }

        showActionStatus("Không thể mở ứng dụng danh bạ")
        Toast.makeText(this, "Không thể mở ứng dụng danh bạ", Toast.LENGTH_SHORT).show()
    }

    private fun openNoteEditor() {
        if (!inCallMode) {
            showActionStatus("Cần kết nối cuộc gọi trước khi ghi chú")
            return
        }

        val noteInput = EditText(this).apply {
            hint = "Nhập ghi chú cuộc gọi..."
            minLines = 3
            maxLines = 6
        }

        AlertDialog.Builder(this)
            .setTitle("Ghi chú cuộc gọi")
            .setView(noteInput)
            .setNegativeButton("Hủy", null)
            .setPositiveButton("Lưu") { _, _ ->
                val noteText = noteInput.text?.toString().orEmpty().trim()
                if (noteText.isBlank()) {
                    showActionStatus("Bạn chưa nhập nội dung ghi chú")
                    Toast.makeText(this, "Vui lòng nhập nội dung ghi chú", Toast.LENGTH_SHORT).show()
                    return@setPositiveButton
                }

                saveCallNote(noteText)
            }
            .show()
    }

    private fun saveCallNote(noteText: String) {
        val outputRoot = getExternalFilesDir(Environment.DIRECTORY_DOCUMENTS) ?: filesDir
        val outputDir = File(outputRoot, "call-notes").apply { mkdirs() }
        val timestamp = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US).format(Date())
        val prettyTime = SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.US).format(Date())
        val outputFile = File(outputDir, "note_$timestamp.txt")
        val caller = callerLabelView.text?.toString().orEmpty().ifBlank { "Không rõ số" }
        val content = buildString {
            appendLine("Thời gian: $prettyTime")
            appendLine("Người gọi: $caller")
            appendLine()
            appendLine(noteText)
        }

        val saved = runCatching {
            outputFile.writeText(content, Charsets.UTF_8)
            true
        }.getOrDefault(false)

        if (saved) {
            showActionStatus("Đã lưu ghi chú: ${outputFile.name}")
            Toast.makeText(this, "Đã lưu ghi chú cuộc gọi", Toast.LENGTH_SHORT).show()
            return
        }

        showActionStatus("Không thể lưu ghi chú cuộc gọi")
        Toast.makeText(this, "Không thể lưu ghi chú cuộc gọi", Toast.LENGTH_SHORT).show()
    }

    private fun extractPhoneNumber(raw: String): String {
        return raw.filter { it.isDigit() || it == '+' }
    }

    private fun resolveDisplayCallerLabel(incomingLabel: String?, storeLabel: String): String {
        val primary = incomingLabel.orEmpty().trim()
        if (primary.isNotBlank() && !isUnknownCallerLabel(primary)) {
            return primary
        }

        val cached = storeLabel.trim()
        if (cached.isNotBlank() && !isUnknownCallerLabel(cached)) {
            return cached
        }

        val activeNumber = resolveCallerNumberFromActiveCall()
        if (activeNumber.isNotBlank()) {
            return activeNumber
        }

        val fallbackNumber = extractPhoneNumber(primary.ifBlank { cached })
        if (fallbackNumber.isNotBlank()) {
            return fallbackNumber
        }

        return "Số đang gọi"
    }

    private fun isUnknownCallerLabel(label: String): Boolean {
        val normalized = label.trim().lowercase(Locale.ROOT)
        return normalized == "unknown caller" ||
            normalized == "người gọi chưa xác định" ||
            normalized == "không rõ số" ||
            normalized == "số đang gọi"
    }

    private fun resolveCallerNumberFromActiveCall(): String {
        val rawNumber = runCatching {
            IncomingActiveCallStore.current()?.details?.handle?.schemeSpecificPart.orEmpty()
        }.getOrDefault("")
        return extractPhoneNumber(rawNumber)
    }

    private fun updateCallerAvatar(callerLabel: String) {
        val phone = extractPhoneNumber(callerLabel)
        if (phone.isBlank() || !hasReadContactsPermission()) {
            callerAvatarView.visibility = View.GONE
            return
        }

        val avatarUri = findContactPhotoUri(phone)
        if (avatarUri == null) {
            callerAvatarView.visibility = View.GONE
            return
        }

        val bitmap = runCatching {
            contentResolver.openInputStream(avatarUri)?.use { BitmapFactory.decodeStream(it) }
        }.getOrNull()

        if (bitmap == null) {
            callerAvatarView.visibility = View.GONE
            return
        }

        callerAvatarView.imageTintList = null
        callerAvatarView.setImageBitmap(bitmap)
        callerAvatarView.visibility = View.VISIBLE
    }

    private fun hasReadContactsPermission(): Boolean {
        return ContextCompat.checkSelfPermission(
            this,
            Manifest.permission.READ_CONTACTS
        ) == PackageManager.PERMISSION_GRANTED
    }

    private fun findContactPhotoUri(phone: String): Uri? {
        val lookupUri = Uri.withAppendedPath(
            ContactsContract.PhoneLookup.CONTENT_FILTER_URI,
            Uri.encode(phone)
        )
        val columns = arrayOf(
            ContactsContract.PhoneLookup.PHOTO_URI,
            ContactsContract.PhoneLookup.PHOTO_THUMBNAIL_URI
        )

        return runCatching {
            contentResolver.query(lookupUri, columns, null, null, null)?.use { cursor ->
                if (!cursor.moveToFirst()) {
                    return@use null
                }

                val photoUri = cursor.getString(0)
                val thumbnailUri = cursor.getString(1)
                val value = photoUri.orEmpty().ifBlank { thumbnailUri.orEmpty() }
                value.takeIf { it.isNotBlank() }?.let(Uri::parse)
            }
        }.getOrNull()
    }

    private fun launchIntentSafely(intent: Intent): Boolean {
        if (intent.resolveActivity(packageManager) == null) {
            return false
        }

        return runCatching {
            startActivity(intent)
            true
        }.getOrDefault(false)
    }

    private fun handleDeclineAction() {
        val isDemo = intent?.getBooleanExtra(com.sixseven.antiscam.incoming.IncomingCallContracts.EXTRA_IS_DEMO, false) ?: false

        if (isDemo) {
            // For demo calls, treat decline as local stop (no telephony interactions)
            val stopIntent = Intent(com.sixseven.antiscam.incoming.IncomingCallContracts.ACTION_DEBUG_STOP_DEMO).apply {
                setPackage(packageName)
            }
            sendBroadcast(stopIntent)
            IncomingCallNotifier.cancelIncomingCall(this)
            IncomingCallStateStore.clear()
            stopRecordingIfNeeded()
            callStateView.text = if (inCallMode) "Đã kết thúc cuộc gọi (Demo)" else "Đã từ chối cuộc gọi (Demo)"
            protectionHintView.text = "Đã đóng màn hình gọi."
            showActionStatus(if (inCallMode) "Đã kết thúc cuộc gọi (Demo)" else "Đã từ chối cuộc gọi (Demo)")
            stopDurationTimer(reset = true)
            finishSafelyDelayed()
            return
        }

        val declined = IncomingCallControl.decline(this)

        if (declined) {
            IncomingCallNotifier.cancelIncomingCall(this)
            IncomingCallStateStore.clear()
            stopRecordingIfNeeded()
            callStateView.text = if (inCallMode) "Đã kết thúc cuộc gọi" else "Đã từ chối cuộc gọi"
            protectionHintView.text = "Đã đóng màn hình gọi."
            showActionStatus(if (inCallMode) "Đã kết thúc cuộc gọi" else "Đã từ chối cuộc gọi")
            stopDurationTimer(reset = true)
            finishSafelyDelayed()
            return
        }

        showActionStatus("Không thể từ chối cuộc gọi trên thiết bị này")
        Toast.makeText(
            this,
            "Không thể từ chối cuộc gọi trên thiết bị này",
            Toast.LENGTH_LONG
        ).show()
    }

    private fun updateCallerFromIntent(sourceIntent: Intent?) {
        val incomingLabel = sourceIntent
            ?.getStringExtra(IncomingCallContracts.EXTRA_CALLER_LABEL)
        val storeLabel = IncomingCallStateStore.currentLabel()
        val callerLabel = resolveDisplayCallerLabel(incomingLabel, storeLabel)

        callerLabelView.text = callerLabel
        callMetaView.text = "$callerLabel | Việt Nam HD"
        updateCallerAvatar(callerLabel)
    }

    private fun applyInitialStateFromIntent(sourceIntent: Intent?) {
        when (sourceIntent?.getStringExtra(IncomingCallContracts.EXTRA_CALL_STATE)) {
            TelephonyManager.EXTRA_STATE_OFFHOOK -> showConnectedUi()
            TelephonyManager.EXTRA_STATE_IDLE -> {
                showRingingUi()
                callStateView.text = "Đã từ chối cuộc gọi"
                protectionHintView.text = "Đang đóng màn hình cuộc gọi..."
                showActionStatus("Đã từ chối từ màn hình ngoài")
                finishSafelyDelayed(300L)
            }

            IncomingCallContracts.STATE_ANSWER_FAILED -> {
                showRingingUi()
                showActionStatus("Không thể trả lời từ màn hình ngoài")
            }

            IncomingCallContracts.STATE_DECLINE_FAILED -> {
                showRingingUi()
                showActionStatus("Không thể từ chối từ màn hình ngoài")
            }

            else -> showRingingUi()
        }
    }

    private fun registerCallStateReceiver() {
        val filter = IntentFilter(IncomingCallContracts.ACTION_CALL_STATE_CHANGED)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            registerReceiver(callStateReceiver, filter, Context.RECEIVER_NOT_EXPORTED)
        } else {
            registerReceiver(callStateReceiver, filter)
        }
    }

    private fun enableLockScreenMode() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O_MR1) {
            setShowWhenLocked(true)
            setTurnScreenOn(true)
        } else {
            @Suppress("DEPRECATION")
            window.addFlags(
                WindowManager.LayoutParams.FLAG_SHOW_WHEN_LOCKED or
                    WindowManager.LayoutParams.FLAG_TURN_SCREEN_ON
            )
        }

        @Suppress("DEPRECATION")
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
    }

    private fun showRingingUi() {
        inCallMode = false
        isOnHold = false
        isSpeakerOn = false
        isMicMuted = false
        stopRecordingIfNeeded()
        resetAudioRouteIfNeeded()
        callStateView.text = "Đang đổ chuông..."
        protectionHintView.text = "Nhấn Trả lời để bắt đầu theo dõi, hoặc Từ chối để ngắt ngay."
        answerButton.text = "Trả lời"
        answerButton.isEnabled = true
        answerButton.alpha = 1f
        incomingDeclineButton.isEnabled = true
        incomingDeclineButton.alpha = 1f
        declineLabelView.text = "Từ chối"
        incomingActionsLayout.visibility = View.VISIBLE
        inCallControlsLayout.visibility = View.GONE
        bottomControlsLayout.visibility = View.GONE
        speakerLabelView.visibility = View.VISIBLE
        speakerButton.visibility = View.VISIBLE
        updateControlButtons()
        stopDurationTimer(reset = false)
        showActionStatus("Sẵn sàng nhận thao tác cuộc gọi")
    }

    private fun showConnectedUi() {
        inCallMode = true
        syncAudioAndHoldState()
        callStateView.text = "Đã kết nối. AI đang theo dõi cuộc gọi..."
        protectionHintView.text = "Nếu thấy bất thường, bấm Kết thúc ngay."
        answerButton.text = "Đã trả lời"
        answerButton.isEnabled = false
        answerButton.alpha = 0.6f
        declineLabelView.text = "Kết thúc"
        incomingActionsLayout.visibility = View.GONE
        inCallControlsLayout.visibility = View.VISIBLE
        bottomControlsLayout.visibility = View.VISIBLE
        speakerButton.visibility = View.VISIBLE
        speakerLabelView.visibility = View.VISIBLE
        updateControlButtons()
        showActionStatus("Cuộc gọi đang hoạt động")

        if (!timerStarted) {
            durationView.base = SystemClock.elapsedRealtime()
            durationView.visibility = View.VISIBLE
            durationView.start()
            timerStarted = true
        }

        // Transcription is provided by the InCall service; activity displays updates via broadcast
        audioCaptureStatusView.text = "Micro: Đang kiểm tra..."
        audioCaptureStatusView.setTextColor(Color.parseColor("#fbbf24"))
    }

    private fun stopDurationTimer(reset: Boolean) {
        durationView.stop()
        durationView.visibility = View.GONE
        if (reset) {
            durationView.base = SystemClock.elapsedRealtime()
        }
        timerStarted = false
    }

    private fun toggleHoldState() {
        if (!inCallMode) {
            showActionStatus("Cần kết nối cuộc gọi trước khi giữ máy")
            return
        }

        val call = IncomingActiveCallStore.current()
        if (call == null) {
            showActionStatus("Không tìm thấy cuộc gọi để giữ máy")
            return
        }

        val currentlyHolding = runCatching { call.state == Call.STATE_HOLDING }.getOrDefault(isOnHold)
        val success = runCatching {
            if (currentlyHolding) {
                call.unhold()
            } else {
                call.hold()
            }
            true
        }.getOrDefault(false)

        if (!success) {
            showActionStatus("Không thể đổi trạng thái giữ máy")
            return
        }

        isOnHold = !currentlyHolding
        updateControlButtons()
        showActionStatus(if (isOnHold) "Đã giữ máy" else "Đã bỏ giữ máy")
    }

    private fun toggleSpeakerState() {
        if (!inCallMode) {
            showActionStatus("Cần kết nối cuộc gọi trước khi bật loa ngoài")
            return
        }

        val manager = audioManager
        if (manager == null) {
            showActionStatus("Không tìm thấy dịch vụ âm thanh")
            return
        }

        val target = !isSpeakerOn
        val serviceRouted = GuardianIncomingInCallService.requestSpeakerRoute(target)
        val legacyRouted = runCatching {
            manager.mode = AudioManager.MODE_IN_COMMUNICATION
            manager.isSpeakerphoneOn = target
            if (target) {
                boostVoiceCallVolume(manager)
            }
            true
        }.getOrDefault(false)

        if (!serviceRouted && !legacyRouted) {
            showActionStatus("Không thể đổi chế độ loa ngoài")
            return
        }

        isSpeakerOn = GuardianIncomingInCallService.isSpeakerRouteEnabled()
            ?: runCatching { manager.isSpeakerphoneOn }.getOrDefault(target)

        updateControlButtons()
        showActionStatus(if (isSpeakerOn) "Đã bật loa ngoài" else "Đã tắt loa ngoài")
    }

    private fun boostVoiceCallVolume(manager: AudioManager) {
        runCatching {
            val stream = AudioManager.STREAM_VOICE_CALL
            val current = manager.getStreamVolume(stream)
            val max = manager.getStreamMaxVolume(stream)
            val target = (max * 0.75f).toInt().coerceAtLeast(current)
            if (target > current) {
                manager.setStreamVolume(stream, target, 0)
            }
        }
    }

    private fun toggleMuteState() {
        if (!inCallMode) {
            showActionStatus("Cần kết nối cuộc gọi trước khi tắt tiếng")
            return
        }

        val manager = audioManager
        val target = !isMicMuted
        val serviceMuted = GuardianIncomingInCallService.requestMicrophoneMute(target)
        val legacyMuted = runCatching {
            if (manager == null) {
                false
            } else {
                manager.mode = AudioManager.MODE_IN_COMMUNICATION
                manager.isMicrophoneMute = target
                true
            }
        }.getOrDefault(false)

        if (!serviceMuted && !legacyMuted) {
            showActionStatus("Không thể đổi chế độ micro")
            return
        }

        isMicMuted = GuardianIncomingInCallService.isMicrophoneMuted()
            ?: runCatching { manager?.isMicrophoneMute == true }.getOrDefault(target)
        updateControlButtons()
        showActionStatus(if (isMicMuted) "Đã tắt tiếng micro" else "Đã mở lại micro")
    }

    private fun toggleRecordingState() {
        if (!inCallMode) {
            showActionStatus("Chỉ ghi âm khi cuộc gọi đã kết nối")
            return
        }

        if (isRecording) {
            stopRecordingIfNeeded()
            return
        }

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            openMainCallSetup()
            return
        }

        startRecordingInternal()
    }

    private fun startRecordingInternal() {
        val outputRoot = getExternalFilesDir(Environment.DIRECTORY_MUSIC) ?: filesDir
        val outputDir = File(outputRoot, "call-recordings").apply { mkdirs() }
        val timestamp = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US).format(Date())
        val outputFile = File(outputDir, "call_$timestamp.m4a")

        val newRecorder = MediaRecorder()
        val started = runCatching {
            newRecorder.setAudioSource(MediaRecorder.AudioSource.VOICE_COMMUNICATION)
            newRecorder.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4)
            newRecorder.setAudioEncoder(MediaRecorder.AudioEncoder.AAC)
            newRecorder.setAudioEncodingBitRate(96000)
            newRecorder.setAudioSamplingRate(44100)
            newRecorder.setOutputFile(outputFile.absolutePath)
            newRecorder.prepare()
            newRecorder.start()
            true
        }.getOrDefault(false)

        if (!started) {
            runCatching { newRecorder.reset() }
            runCatching { newRecorder.release() }
            runCatching { outputFile.delete() }
            showActionStatus("Không thể bật ghi âm trên thiết bị này")
            return
        }

        recorder = newRecorder
        recordingFile = outputFile
        isRecording = true
        updateControlButtons()
        showActionStatus("Đang ghi âm: ${outputFile.name}")
    }

    private fun stopRecordingIfNeeded() {
        if (!isRecording) {
            return
        }

        val activeRecorder = recorder
        val fileName = recordingFile?.name
        val stopped = runCatching {
            activeRecorder?.stop()
            true
        }.getOrDefault(false)

        runCatching { activeRecorder?.reset() }
        runCatching { activeRecorder?.release() }

        recorder = null
        isRecording = false
        updateControlButtons()

        if (!stopped) {
            runCatching { recordingFile?.delete() }
            recordingFile = null
            showActionStatus("Ghi âm thất bại")
            return
        }

        showActionStatus("Đã lưu ghi âm: $fileName")
        recordingFile = null
    }

    private fun openMainCallSetup() {
        val intent = Intent(this, com.sixseven.antiscam.MainActivity::class.java).apply {
            addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_SINGLE_TOP)
            putExtra("open_call_setup", true)
        }
        startActivity(intent)
        showActionStatus("Vui lòng cấp quyền micro trong tab Call Setup trên trang chính.")
        Toast.makeText(this, "Cần cấp quyền Micro; mở trang Cấp quyền.", Toast.LENGTH_LONG).show()
    }

    
    

    private fun syncAudioAndHoldState() {
        val manager = audioManager
        isSpeakerOn = GuardianIncomingInCallService.isSpeakerRouteEnabled()
            ?: runCatching { manager?.isSpeakerphoneOn == true }.getOrDefault(false)
        isMicMuted = GuardianIncomingInCallService.isMicrophoneMuted()
            ?: runCatching { manager?.isMicrophoneMute == true }.getOrDefault(false)
        isOnHold = runCatching {
            IncomingActiveCallStore.current()?.state == Call.STATE_HOLDING
        }.getOrDefault(false)
    }

    private fun resetAudioRouteIfNeeded() {
        val manager = audioManager ?: return
        runCatching {
            GuardianIncomingInCallService.requestSpeakerRoute(false)
            GuardianIncomingInCallService.requestMicrophoneMute(false)
            manager.isSpeakerphoneOn = false
            manager.isMicrophoneMute = false
        }
    }

    private fun updateControlButtons() {
        holdLabelView.text = if (isOnHold) "Bỏ giữ" else "Giữ"
        speakerLabelView.text = if (isSpeakerOn) "Tắt loa" else "Loa ngoài"
        muteLabelView.text = if (isMicMuted) "Mở mic" else "Tắt tiếng"
        recordLabelView.text = if (isRecording) "Dừng ghi" else "Ghi âm"

        updateToggleButtonVisual(holdButton, isOnHold)
        updateToggleButtonVisual(speakerButton, isSpeakerOn)
        updateToggleButtonVisual(muteButton, isMicMuted)

        if (isRecording) {
            recordButton.setBackgroundResource(R.drawable.bg_call_action_circle_active)
            recordButton.setColorFilter(Color.parseColor("#fecaca"))
        } else {
            recordButton.setBackgroundResource(R.drawable.bg_call_action_circle)
            recordButton.setColorFilter(Color.WHITE)
        }
    }

    private fun updateToggleButtonVisual(button: ImageButton, active: Boolean) {
        if (active) {
            button.setBackgroundResource(R.drawable.bg_call_action_circle_active)
            button.setColorFilter(Color.parseColor("#bbf7d0"))
            return
        }

        button.setBackgroundResource(R.drawable.bg_call_action_circle)
        button.setColorFilter(Color.WHITE)
    }

    private fun showActionStatus(message: String) {
        actionStatusView.text = message
    }

    private fun finishSafelyDelayed(delayMs: Long = 450L) {
        window.decorView.postDelayed({ finish() }, delayMs)
    }
}
