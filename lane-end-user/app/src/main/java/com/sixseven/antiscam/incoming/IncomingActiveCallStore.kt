package com.sixseven.antiscam.incoming

import android.telecom.Call

object IncomingActiveCallStore {
    private val lock = Any()
    private var activeCall: Call? = null

    fun attach(call: Call) {
        synchronized(lock) {
            activeCall = call
        }
    }

    fun current(): Call? = synchronized(lock) { activeCall }

    fun clear(call: Call? = null) {
        synchronized(lock) {
            if (call == null || activeCall === call) {
                activeCall = null
            }
        }
    }
}
