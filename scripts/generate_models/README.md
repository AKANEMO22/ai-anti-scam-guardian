# generate_models (tạo file model lớn dạng placeholder)

Thư mục này chứa các script giúp tạo các file model lớn (ví dụ `.tflite`) cho mục đích test/cục bộ, và helper để chuẩn bị repository trước khi `git push` (loại bỏ file lớn khỏi index / thêm `.gitignore`).

Hướng dẫn nhanh

- Tạo file `.tflite` placeholder (mặc định 5 MB):

  PowerShell / CMD:

  ```powershell
  python scripts/generate_models/generate_tflite.py --output lane-end-user/core/ml/src/main/assets/scam_detector_en.tflite --size-mb 5
  ```

  Bash / WSL:

  ```bash
  python3 scripts/generate_models/generate_tflite.py -o lane-end-user/core/ml/src/main/assets/scam_detector_en.tflite -s 5
  ```

- Chuẩn bị repo trước khi push (PowerShell):

  ```powershell
  # Sinh file (tuỳ chọn) và cập nhật .gitignore; nếu repo có lịch sử chứa .tflite script sẽ cảnh báo
  scripts/generate_models/prepare_repo_for_push.ps1 -OutputPath lane-end-user/core/ml/src/main/assets/scam_detector_en.tflite -SizeMB 5
  ```

  Để tự động push sau khi xử lý, thêm option `-AutoPush` (chú ý: nếu repo chứa .tflite trong lịch sử, script sẽ cảnh báo và không push trừ khi bạn rõ ràng yêu cầu).

Lưu ý quan trọng

- Nếu các file lớn (.tflite) đã được committed vào lịch sử của branch bạn đang cố gắng push, GitHub có thể từ chối push ngay cả khi bạn xóa file ở commit cuối. Trong trường hợp đó bạn cần dùng `git lfs migrate import --include="*.tflite"` hoặc công cụ `git-filter-repo` / BFG để sửa lại lịch sử, sau đó force-push (thao tác nguy hiểm — phối hợp với team).

- Mặc định script tạo file tối đa 500MB trừ khi bạn thêm `--force`.

-- Tải models từ remote storage:

  ```powershell
  # Sử dụng file cấu hình mẫu scripts/generate_models/models_to_fetch.json
  python scripts/generate_models/fetch_models.py --config scripts/generate_models/models_to_fetch.json
  # hoặc PowerShell wrapper
  scripts/generate_models/fetch_models.ps1 -Config scripts/generate_models/models_to_fetch.json
  ```

-- Tạo và push nhánh snapshot `main-up` (không chứa file lớn):

  ```powershell
  # Tạo snapshot loại bỏ *.tflite và push nhánh main-up lên origin (AN TOÀN)
  scripts/git/create_and_push_main_up.ps1

  # Nếu muốn thay thế remote 'main' bằng snapshot này (CẢNH BÁO: destructive),
  # re-run with ForceReplaceMain
  scripts/git/create_and_push_main_up.ps1 -ForceReplaceMain
  ```

