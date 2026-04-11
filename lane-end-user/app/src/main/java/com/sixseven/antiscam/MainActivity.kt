package com.sixseven.antiscam

import android.animation.ObjectAnimator
import android.animation.ValueAnimator
import android.app.NotificationManager
import android.graphics.Color
import android.os.Build
import android.os.Bundle
import android.view.MotionEvent
import android.view.View
import android.widget.ScrollView
import android.widget.TextView
import android.view.animation.AccelerateDecelerateInterpolator
import android.view.animation.OvershootInterpolator
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.updatePadding
import com.sixseven.antiscam.dialer.permissions.CallPermissionManager
import com.sixseven.antiscam.dialer.role.DefaultDialerRoleHelper
import com.sixseven.antiscam.dialer.setup.DialerSetupGuideDialog

class MainActivity : AppCompatActivity() {

    private lateinit var tabs: List<TextView>
    private lateinit var contentScroll: ScrollView
    private lateinit var tabSections: Map<Int, List<View>>
    private var setupGuideShownInSession = false

    private val defaultDialerRoleLauncher =
        registerForActivityResult(ActivityResultContracts.StartActivityForResult()) {
            if (!DefaultDialerRoleHelper.isDefaultDialer(this)) {
                showDialerSetupGuide()
            }
        }

    private val callPermissionLauncher =
        registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) {
            if (CallPermissionManager.hasAllPermissions(this)) {
                ensureDefaultDialerRole()
            } else {
                showDialerSetupGuide()
            }
        }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        applySystemInsets()
        setupSections()
        runEntryAnimation()
        runShieldPulseAnimation()
        runCardStaggerAnimation()
        setupTabs()
        attachPressScaleAnimation()
        ensureCallPermissionsAndDialer()
    }

    override fun onResume() {
        super.onResume()
        if (DefaultDialerRoleHelper.isDefaultDialer(this)) {
            setupGuideShownInSession = false
        }
    }

    private fun ensureDefaultDialerRole() {
        if (DefaultDialerRoleHelper.isDefaultDialer(this)) {
            if (!canShowIncomingPopupOverApps()) {
                showDialerSetupGuide()
            }
            return
        }

        val roleIntent = DefaultDialerRoleHelper.buildRoleRequestIntent(this)
        if (roleIntent != null) {
            runCatching {
                defaultDialerRoleLauncher.launch(roleIntent)
            }.onFailure {
                showDialerSetupGuide()
            }
        } else {
            showDialerSetupGuide()
        }
    }

    private fun canShowIncomingPopupOverApps(): Boolean {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.UPSIDE_DOWN_CAKE) {
            return true
        }

        val manager = getSystemService(NotificationManager::class.java)
        return manager.canUseFullScreenIntent()
    }

    private fun ensureCallPermissionsAndDialer() {
        if (!CallPermissionManager.hasAllPermissions(this)) {
            callPermissionLauncher.launch(CallPermissionManager.requiredPermissions())
            return
        }

        ensureDefaultDialerRole()
    }

    private fun showDialerSetupGuide() {
        if (setupGuideShownInSession) {
            val opened = DefaultDialerRoleHelper.openDefaultAppSettings(this)
            if (!opened) {
                DefaultDialerRoleHelper.openAppDetailsSettings(this)
            }
            return
        }

        setupGuideShownInSession = true
        DialerSetupGuideDialog.show(this)
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
            R.id.cardRisk,
            R.id.cardSnapshot,
            R.id.cardActions,
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
            findViewById(R.id.btnScan),
            findViewById(R.id.btnCall),
            findViewById(R.id.btnHistory),
            findViewById(R.id.btnGuardian),
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

        findViewById<View>(R.id.btnScan).setOnClickListener { setActiveTab(findViewById(R.id.tabScan)) }
        findViewById<View>(R.id.btnCall).setOnClickListener { ensureCallPermissionsAndDialer() }
        findViewById<View>(R.id.btnHistory).setOnClickListener { setActiveTab(findViewById(R.id.tabHistory)) }
        findViewById<View>(R.id.btnGuardian).setOnClickListener { setActiveTab(findViewById(R.id.tabGuardian)) }

        setActiveTab(findViewById(R.id.tabHome))
    }

    private fun setupSections() {
        contentScroll = findViewById(R.id.scrollContent)

        val homeViews = listOf(
            findViewById<View>(R.id.cardRisk),
            findViewById<View>(R.id.cardSnapshot),
            findViewById<View>(R.id.cardActions),
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
}
