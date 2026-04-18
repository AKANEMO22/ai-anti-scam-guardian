param(
    [string]$ApkPath = "lane-end-user/app/build/outputs/apk/debug/app-debug.apk",
    [int]$TimeoutPerAttemptSec = 90,
    [int]$Attempts = 3
)

$infinite = $false
if ($Attempts -le 0) { $infinite = $true }

Write-Host "Auto transcription test script"

# find connected device
$dev = (adb devices | Select-String '\tdevice' | ForEach-Object { ($_ -split '\s+')[0] } | Select-Object -First 1)
if (-not $dev) {
    Write-Error "No adb device found"
    exit 1
}
Write-Host "Using device: $dev"

# ensure APK exists
if (-not (Test-Path $ApkPath)) {
    Write-Error "APK not found at $ApkPath"
    exit 1
}

# install apk (idempotent)
Write-Host "Installing APK: $ApkPath"
adb -s $dev install -r $ApkPath 2>&1 | ForEach-Object { Write-Host $_ }

# grant common runtime permissions
$perms = @(
    "android.permission.RECORD_AUDIO",
    "android.permission.READ_CALL_LOG",
    "android.permission.READ_SMS",
    "android.permission.READ_CONTACTS",
    "android.permission.ANSWER_PHONE_CALLS",
    "android.permission.POST_NOTIFICATIONS",
    "android.permission.READ_PHONE_STATE"
)
foreach ($p in $perms) {
    Write-Host "Granting: $p"
    try { adb -s $dev shell pm grant com.sixseven.antiscam $p 2>&1 | ForEach-Object { Write-Host $_ } } catch { }
}

# helper to set appops variants
function Try-AppOpsSet($variant) {
    Write-Host "Trying appops variant: $variant"
    try {
        adb -s $dev shell appops set com.sixseven.antiscam $variant allow 2>&1 | ForEach-Object { Write-Host $_ }
    } catch { }
}

$found = $false
$i = 1
while ($infinite -or $i -le $Attempts) {
    Write-Host "\n=== Attempt $i of $Attempts ==="

    switch ($i) {
        1 { Try-AppOpsSet "RECORD_AUDIO" }
        2 { Try-AppOpsSet "android:record_audio" }
        3 { Try-AppOpsSet "RECORD_AUDIO"; Try-AppOpsSet "android:record_audio" }
    }

    # clear logcat
    Write-Host "Clearing logcat buffer"
    adb -s $dev logcat -c 2>&1 | ForEach-Object { }

    # start app main activity to ensure services initialize
    Write-Host "Starting app main activity"
    adb -s $dev shell am start -a android.intent.action.MAIN -n com.sixseven.antiscam/.MainActivity 2>&1 | ForEach-Object { }
    Start-Sleep -Seconds 2
    # start incoming UI (so transcript view is visible)
    Write-Host "Starting IncomingCallActivity (demo connected state)"
    adb -s $dev shell am start -n com.sixseven.antiscam/.incoming.IncomingCallActivity --es extra_call_state "OFFHOOK" 2>&1 | ForEach-Object { }
    Start-Sleep -Seconds 1

    # send debug broadcast to start STT (MainActivity handles this in debugReceiver)
    Write-Host "Sending DEBUG_START_STT broadcast"
    adb -s $dev shell am broadcast -a com.sixseven.antiscam.action.DEBUG_START_STT -p com.sixseven.antiscam 2>&1 | ForEach-Object { Write-Host $_ }

    # Generate demo TTS audio locally, push to device, and play it
    $localDemo = Join-Path $PWD "demo_call.wav"
    Write-Host "Generating demo TTS to: $localDemo"
    try {
        Add-Type -AssemblyName System.speech
        $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
        $synth.Rate = -1
        $synth.Volume = 90
        $synth.SetOutputToWaveFile($localDemo)
        $ttsText = "Xin chào. Đây là cuộc gọi thử. Tôi đang nói để kiểm tra chức năng chuyển văn bản."
        $synth.Speak($ttsText)
        $synth.Dispose()
    } catch {
        Write-Warning "TTS generation failed: $_"
    }

    Write-Host "Pushing demo audio to device"
    adb -s $dev push $localDemo /sdcard/Download/demo_call.wav 2>&1 | ForEach-Object { Write-Host $_ }

    Write-Host "Playing demo audio on device"
    adb -s $dev shell am start -a android.intent.action.VIEW -d file:///sdcard/Download/demo_call.wav -t audio/wav 2>&1 | ForEach-Object { Write-Host $_ }

    # monitor UI (uiautomator dump) and logs for transcription
    $end = (Get-Date).AddSeconds($TimeoutPerAttemptSec)
    while ((Get-Date) -lt $end) {
        # check logs first for transcript broadcasts
        $out = adb -s $dev logcat -d -v time 2>&1
        if ($out -match "ACTION_TRANSCRIPTION_UPDATED" -or $out -match "broadcastTranscript") {
            Write-Host "Found transcription-related logs"
            $out -split "`n" | Where-Object { $_ -match "broadcastTranscript|ACTION_TRANSCRIPTION_UPDATED" } | ForEach-Object { Write-Host $_ }
        }

        # dump UI and inspect tvTranscript
        adb -s $dev shell uiautomator dump /sdcard/window_dump.xml 2>&1 | ForEach-Object { }
        adb -s $dev pull /sdcard/window_dump.xml ./window_dump.xml 2>&1 | ForEach-Object { }
        $dump = Get-Content ./window_dump.xml -Raw -ErrorAction SilentlyContinue
        if ($dump) {
            $m = [regex]::Match($dump, 'resource-id="com.sixseven.antiscam:id/tvTranscript"[^"]*text="([^"]*)"')
            if ($m.Success) {
                $txt = $m.Groups[1].Value
                if ($txt -and $txt.Trim().Length -gt 0) {
                    Write-Host "Transcript detected in UI: $txt"
                    $found = $true
                    break
                }
            }
        }

        Start-Sleep -Seconds 2
    }

    if ($found) { break }
    Write-Host "No transcription events in attempt $i"
    $i++
}

if ($found) {
    Write-Host "SUCCESS: transcription events observed"
    exit 0
} else {
    Write-Host "FAIL: no transcription events detected after $Attempts attempts"
    Write-Host "Gathering diagnostics..."
    adb -s $dev shell appops get com.sixseven.antiscam 2>&1 | ForEach-Object { Write-Host $_ }
    adb -s $dev shell dumpsys package com.sixseven.antiscam 2>&1 | ForEach-Object { Write-Host $_ }
    adb -s $dev logcat -d -v time | Select-String -Pattern "AppOps|AppsFilter|RECORD_AUDIO|TranscriptionManager|TRANSCRIPTION_STATUS|ACTION_TRANSCRIPTION_UPDATED|broadcastTranscript" | ForEach-Object { Write-Host $_ }
    exit 2
}
