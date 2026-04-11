@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM Usage:
REM   - Double click: build Debug APK
REM   - CMD: build_apk.bat release

set "PROJECT_DIR=%~dp0"
if not exist "%PROJECT_DIR%settings.gradle.kts" (
  echo [ERROR] settings.gradle.kts not found in this folder.
  pause
  exit /b 1
)

set "BUILD_TYPE=debug"
set "GRADLE_TASK=assembleDebug"
if /I "%~1"=="release" (
  set "BUILD_TYPE=release"
  set "GRADLE_TASK=assembleRelease"
)

set "OUTPUT_BASE=%PROJECT_DIR%apk-output"
if not exist "%OUTPUT_BASE%" mkdir "%OUTPUT_BASE%"

echo [INFO] Build task: %GRADLE_TASK%

set "NEED_WRAPPER_BOOTSTRAP=0"
if not exist "%PROJECT_DIR%gradlew.bat" set "NEED_WRAPPER_BOOTSTRAP=1"
if not exist "%PROJECT_DIR%gradle\wrapper\gradle-wrapper.jar" set "NEED_WRAPPER_BOOTSTRAP=1"
if not exist "%PROJECT_DIR%gradle\wrapper\gradle-wrapper.properties" set "NEED_WRAPPER_BOOTSTRAP=1"

if "%NEED_WRAPPER_BOOTSTRAP%"=="1" (
  echo [INFO] Gradle wrapper files missing. Bootstrapping...
  if not exist "%PROJECT_DIR%gradle\wrapper" mkdir "%PROJECT_DIR%gradle\wrapper"

  powershell -NoProfile -ExecutionPolicy Bypass -Command "try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/gradle/gradle/v8.9.0/gradlew.bat' -OutFile '%PROJECT_DIR%gradlew.bat'; Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/gradle/gradle/v8.9.0/gradlew' -OutFile '%PROJECT_DIR%gradlew'; Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/gradle/gradle/v8.9.0/gradle/wrapper/gradle-wrapper.jar' -OutFile '%PROJECT_DIR%gradle\wrapper\gradle-wrapper.jar'; exit 0 } catch { Write-Error $_; exit 1 }"
  if errorlevel 1 (
    echo [ERROR] Failed to bootstrap Gradle Wrapper.
    echo [HINT] Check internet connection and try again.
    pause
    exit /b 1
  )

  > "%PROJECT_DIR%gradle\wrapper\gradle-wrapper.properties" (
    echo distributionBase=GRADLE_USER_HOME
    echo distributionPath=wrapper/dists
    echo zipStoreBase=GRADLE_USER_HOME
    echo zipStorePath=wrapper/dists
    echo distributionUrl=https\://services.gradle.org/distributions/gradle-8.9-bin.zip
  )
)

pushd "%PROJECT_DIR%"
call gradlew.bat clean %GRADLE_TASK%
if errorlevel 1 (
  popd
  echo [ERROR] Build failed.
  pause
  exit /b 1
)
popd

for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set "TS=%%i"
set "DEST_DIR=%OUTPUT_BASE%\%BUILD_TYPE%_%TS%"
mkdir "%DEST_DIR%" >nul 2>&1

set "APK_COUNT=0"
for /r "%PROJECT_DIR%lane-end-user\app\build\outputs\apk" %%F in (*.apk) do (
  copy /Y "%%F" "%DEST_DIR%\" >nul
  set /a APK_COUNT+=1
)

if "!APK_COUNT!"=="0" (
  echo [ERROR] Build finished but no APK found.
  echo Checked: %PROJECT_DIR%lane-end-user\app\build\outputs\apk
  pause
  exit /b 1
)

echo build_type=%BUILD_TYPE%> "%DEST_DIR%\build-info.txt"
echo build_task=%GRADLE_TASK%>> "%DEST_DIR%\build-info.txt"
echo apk_count=!APK_COUNT!>> "%DEST_DIR%\build-info.txt"
echo generated_at=%TS%>> "%DEST_DIR%\build-info.txt"

echo [OK] APK export done: !APK_COUNT! file(s)
echo [OK] Output folder: %DEST_DIR%
start "" "%DEST_DIR%"

exit /b 0
