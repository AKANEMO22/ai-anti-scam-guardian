pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "AntiScamGuardianAndroid"

include(":app")
project(":app").projectDir = file("lane-end-user/app")

include(":core:common")
project(":core:common").projectDir = file("shared/core/common")

include(":core:ui")
project(":core:ui").projectDir = file("lane-end-user/core/ui")

include(":core:network")
project(":core:network").projectDir = file("lane-api-gateway/core/network")

include(":core:ml")
project(":core:ml").projectDir = file("lane-end-user/core/ml")

include(":domain")
project(":domain").projectDir = file("lane-agentic-core/domain")

include(":data")
project(":data").projectDir = file("lane-agentic-core/data")

include(":feature:dashboard")
project(":feature:dashboard").projectDir = file("lane-end-user/feature/dashboard")

include(":feature:scan")
project(":feature:scan").projectDir = file("lane-end-user/feature/scan")

include(":feature:callshield")
project(":feature:callshield").projectDir = file("lane-end-user/feature/callshield")

include(":feature:warning")
project(":feature:warning").projectDir = file("lane-end-user/feature/warning")

include(":feature:history")
project(":feature:history").projectDir = file("lane-end-user/feature/history")

include(":feature:guardian")
project(":feature:guardian").projectDir = file("lane-end-user/feature/guardian")

include(":feature:settings")
project(":feature:settings").projectDir = file("lane-end-user/feature/settings")

include(":service:background")
project(":service:background").projectDir = file("lane-end-user/service/background")

include(":service:realtimecall")
project(":service:realtimecall").projectDir = file("lane-end-user/service/realtimecall")

include(":service:feedbacksync")
project(":service:feedbacksync").projectDir = file("lane-end-user/service/feedbacksync")
