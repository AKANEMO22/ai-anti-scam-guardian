plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
}

android {
    namespace = "com.sixseven.antiscam"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.sixseven.antiscam"
        minSdk = 26
        targetSdk = 35
        versionCode = 13
        versionName = "0.11.2"
        buildConfigField("String", "API_GATEWAY_BASE_URL", "\"http://10.0.2.2:5002\"")
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }

    buildFeatures {
        buildConfig = true
    }
}

dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.appcompat)
    implementation(libs.google.material)
    implementation(libs.androidx.work.runtime.ktx)

    implementation(project(":core:common"))
    implementation(project(":core:ui"))
    implementation(project(":core:network"))
    implementation(project(":core:ml"))
    implementation(project(":domain"))
    implementation(project(":data"))

    implementation(project(":feature:dashboard"))
    implementation(project(":feature:scan"))
    implementation(project(":feature:callshield"))
    implementation(project(":feature:warning"))
    implementation(project(":feature:history"))
    implementation(project(":feature:guardian"))
    implementation(project(":feature:settings"))

    implementation(project(":service:background"))
    implementation(project(":service:realtimecall"))
    implementation(project(":service:feedbacksync"))
}
