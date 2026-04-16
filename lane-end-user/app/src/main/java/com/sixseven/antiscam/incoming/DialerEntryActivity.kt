package com.sixseven.antiscam.incoming

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.sixseven.antiscam.MainActivity

class DialerEntryActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        routeToMain()
        finish()
    }

    private fun routeToMain() {
        val launchIntent = Intent(this, MainActivity::class.java).apply {
            action = intent?.action
            data = intent?.data
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP)
            addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP)
        }
        startActivity(launchIntent)
    }
}
