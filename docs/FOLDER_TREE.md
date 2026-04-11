# Folder Tree (Pipeline-Aligned)

android-anti-scam-guardian/
- README.md
- settings.gradle.kts
- build.gradle.kts
- gradle.properties
- gradle/libs.versions.toml
- docs/
  - PIPELINE_MAPPING.md
  - FILE_ROLES.md
  - FOLDER_TREE.md

- lane-end-user/
  - app/
    - build.gradle.kts
    - proguard-rules.pro
    - src/main/AndroidManifest.xml
    - src/main/java/com/sixseven/antiscam/GuardianApp.kt
    - src/main/java/com/sixseven/antiscam/MainActivity.kt
    - src/main/java/com/sixseven/antiscam/navigation/AppNavGraph.kt
    - src/main/res/xml/network_security_config.xml
  - core/
    - ui/
      - build.gradle.kts
      - src/main/java/com/sixseven/antiscam/core/ui/DesignTokens.kt
    - ml/
      - build.gradle.kts
      - src/main/java/com/sixseven/antiscam/core/ml/OnDeviceFilter.kt
  - feature/
    - dashboard/
    - scan/
    - callshield/
    - warning/
    - history/
    - guardian/
    - settings/
  - service/
    - background/
    - realtimecall/
    - feedbacksync/
  - assets/
    - audio/
      - scam_call.wav
      - real_call.wav
      - scam_call_sample.wav
      - real_call_sample.wav

- lane-api-gateway/
  - core/
    - network/
      - build.gradle.kts
      - src/main/java/com/sixseven/antiscam/core/network/CloudApi.kt
  - firebase/

- lane-agentic-core/
  - domain/
    - build.gradle.kts
    - src/main/java/com/sixseven/antiscam/domain/model/*
    - src/main/java/com/sixseven/antiscam/domain/usecase/*
  - data/
    - build.gradle.kts
    - src/main/java/com/sixseven/antiscam/data/local/*
    - src/main/java/com/sixseven/antiscam/data/remote/*
    - src/main/java/com/sixseven/antiscam/data/repository/*

- shared/
  - core/
    - common/
      - build.gradle.kts
      - src/main/java/com/sixseven/antiscam/core/common/DispatchersProvider.kt
  - contracts/
    - openapi/cloudrun-api.yaml
    - event-schema/feedback-event.json

- ops/
  - scripts/
    - README.md
