# BÁO CÁO KỸ THUẬT: AI ANTI-SCAM GUARDIAN
## Hệ Thống Bảo Vệ Người Dùng Đa Lớp Dựa Trên Agentic AI

**Đội thi:** [Tên đội thi của bạn]
**Giai đoạn:** Vòng 2 - Phát triển và Thử nghiệm sản phẩm

---

## 1. Phương pháp tiếp cận (Approach)

Dự án **AI Anti-Scam Guardian** được xây dựng với mục tiêu giải quyết vấn đề lừa đảo qua mạng ngày càng tinh vi. Chúng tôi đã chọn một hướng tiếp cận hiện đại, tập trung vào tính linh hoạt và khả năng mở rộng:

### 1.1. Kiến trúc Micro-Lane (Micro-Lane Architecture)
Thay vì xây dựng một hệ thống monolithic cồng kềnh, chúng tôi chia hệ thống thành 4 "Lane" (đường ống) độc lập: **API Gateway, Agentic Core, Storage**, và **End User**. Mỗi Lane đảm nhận một vai trò cụ thể, giao tiếp qua các contract API chặt chẽ, cho phép phát triển và triển khai độc lập.

### 1.2. Hệ Thống Đa Agent (Multi-Agent Collaboration)
Chúng tôi không tin rằng một mô hình AI duy nhất có thể giải quyết mọi hình thức lừa đảo. Do đó, hệ thống sử dụng nhiều Agent phối hợp:
- **Deepfake Agent**: Chuyên phân tích các dấu hiệu giả mạo giọng nói/hình ảnh.
- **Threat Agent**: Phân tích hành vi và áp lực tâm lý trong giao tiếp.
- **Entity Agent**: Trích xuất các thông tin định danh (số điện thoại, link URL, số tài khoản).

### 1.3. Cơ chế RAG (Retrieval-Augmented Generation)
Để AI không chỉ dừng lại ở kiến thức nền, chúng tôi tích hợp kho dữ liệu **Scam Patterns** thông qua Vector Database. Khi gặp một tín hiệu khả nghi, hệ thống sẽ thực hiện tìm kiếm ngữ cảnh nhằm cung cấp bằng chứng thực tế về các kịch bản lừa đảo tương tự.

---

## 2. Kiến trúc hệ thống (System Architecture)

Hệ thống được thiết kế theo mô hình phân tán, tối ưu cho việc triển khai trên hạ tầng Cloud (Google Cloud Platform/Vertex AI).

### 2.1. Sơ đồ luồng dữ liệu (Data Flow)
1. **End User Lane (Android)**: Giám sát các tín hiệu đầu vào (SMS, Call logs) và gửi về API Gateway.
2. **API Gateway**: Thực hiện xác thực (Firebase Auth), kiểm tra Cache (Redis) để giảm độ trễ và điều phối yêu cầu sang Agentic Core.
3. **Agentic AI Core**: Sử dụng **LangGraph** để điều phối luồng suy luận. Signal được phân tích song song bởi các Agent, sau đó **Decision & Reasoning Engine (Gemini 1.5)** sẽ tổng hợp và đưa ra lời giải thích chi tiết.
4. **Storage Lane**: Lưu trữ và truy vấn dữ liệu mẫu (Vertex AI Search) và quản lý phản hồi (Feedback) từ người dùng để cải thiện mô hình.

### 2.2. Công nghệ chủ chốt
- **Language Models**: Google Gemini 1.5 Pro/Flash.
- **Backend Framework**: Python FastAPI.
- **Mobile Framework**: Flutter.
- **Orchestration**: Docker Compose cho local development và Cloud Run cho production.

---

## 3. Các thử nghiệm đã thực hiện (Experiments)

Trong giai đoạn này, chúng tôi tập trung vào việc định lượng khả năng của hệ thống thông qua các bài kiểm tra thực tế.

### 3.1. Benchmarking với tập dữ liệu thực tế
Chúng tôi đã sử dụng bộ dữ liệu chuyên dụng từ dự án `ai-in-the-loop` (khoảng 50 mẫu chat lừa đảo) để chạy script `benchmark_orchestrator.py`. Mục tiêu là đo lường khả năng phân loại của hệ thống trong môi trường không có sự can thiệp của con người.

### 3.2. Thử nghiệm tích hợp (End-to-End Integration)
Chúng tôi đã triển khai toàn bộ stack kỹ thuật bằng Docker Compose, mô phỏng các kết nối thực tế giữa 3 Lane Backend (Ports 8100, 8101, 8102). Việc này giúp đảm bảo các Contract dữ liệu (`SignalPayload`, `ScamScoreResponse`) hoạt động đồng bộ.

---

## 4. Kết quả và đánh giá (Results & Evaluation)

### 4.1. Kết quả định lượng (Metrics)
Dựa trên kết quả benchmark mới nhất:
- **Accuracy**: 46.0%
- **Precision**: 50.0%
- **F1-Score**: 0.07 (Kết quả sơ bộ trên tập dữ liệu khó)
- **Latenncy (Average)**: ~18-20s (bao gồm thời gian gọi API của các Agent).

### 4.2. Đánh giá ưu điểm
- **Khả năng giải thích (Explainability)**: Đây là điểm mạnh nhất của hệ thống. Thay vì chỉ đưa ra con số 0 hay 1, Decision Engine cung cấp các lập luận logic tại sao một tin nhắn/cuộc gọi là lừa đảo.
- **Tính linh hoạt**: Kiến trúc Lane cho phép chúng tôi thay thế hoặc nâng cấp từng Agent mà không ảnh hưởng đến toàn bộ hệ thống.

### 4.3. Hạn chế và hướng phát triển
- **Độ chính xác chưa cao ở chế độ Zero-shot**: Kết quả Benchmark cho thấy cần phải làm tốt hơn khâu nạp dữ liệu vào Vector DB để RAG phát huy hiệu quả.
- **Độ trễ**: Việc sử dụng Multi-Agent làm tăng thời gian phản hồi. Hướng xử lý: Áp dụng xử lý luồng (streaming) và Agentic parallel execution mạnh mẽ hơn.

---
*Báo cáo này được chuẩn bị nhằm mục đích trình bày tiến độ và khả năng thực thi kỹ thuật của đội thi trong khuôn khổ cuộc thi.*
