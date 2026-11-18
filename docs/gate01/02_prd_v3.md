# PRD v3 — SC-04: SentinelIoT
*AI Agent Phát Hiện Bất Thường Cảm Biến IoT (Rò Gas, Cháy, Ngập Nước)*

---

## 1. Bối cảnh và mục tiêu

**Bối cảnh:** Ban quản lý (BQL) tòa nhà hiện nhận cảnh báo từ cảm biến khói/gas/nhiệt/nước rời rạc theo từng điểm, không có hệ thống phân tích tương quan. Khi 1 cảm biến lỗi/báo trễ nhưng cảm biến khác cùng khu đã có tín hiệu bất thường, BQL không biết để xử lý sớm. Ngược lại, rule đơn lẻ (cảm biến nhạy do bụi/hơi nước) gây báo động nhiễu, khiến đội kỹ thuật mất tin tưởng vào hệ thống.

**Mục tiêu dự án:**
1. Xây dựng AI Agent tương quan đa cảm biến, phát hiện sớm nguy cơ cháy và rò gas.
2. Mọi lệnh điều khiển vật lý phải qua người duyệt (HITL), trừ ngưỡng nguy hiểm tính mạng đã định trước.
3. Cung cấp dashboard 2 vai trò (Cư dân / Kỹ thuật BQL) để giám sát và xử lý sự cố.
4. Chứng minh được bằng số liệu đo được (không chỉ demo bằng mắt) rằng hệ thống cân bằng giữa phát hiện đúng và không báo nhiễu.

---

## 2. Người dùng và tình huống sử dụng

**Người dùng chính:** Kỹ thuật viên Ban quản lý tòa nhà. **Người dùng phụ:** Cư dân (chỉ xem, không điều khiển).

| # | Tình huống |
|---|---|
| 1 | Là **kỹ thuật viên BQL**, tôi muốn **thấy ngay khi 2 cảm biến cùng khu báo bất thường cùng lúc (ví dụ nhiệt + khói)**, để **phát hiện nguy cơ cháy sớm hơn là chờ từng cảm biến báo riêng lẻ**. |
| 2 | Là **kỹ thuật viên BQL**, tôi muốn **thấy rõ dữ liệu gốc và lý do suy luận trước khi duyệt một lệnh đóng van/ngắt điện**, để **không phải "tin mù" vào quyết định của agent**. |
| 3 | Là **kỹ thuật viên BQL**, tôi muốn **hệ thống tự phân biệt được dao động bình thường theo giờ/ngày của từng khu với bất thường thật**, để **không bị làm phiền bởi báo động nhiễu liên tục**. |
| 4 | Là **cư dân**, tôi muốn **nhận cảnh báo kèm hướng dẫn xử lý bằng tiếng Việt dễ hiểu khi khu tôi có nguy cơ**, để **biết nên làm gì (ví dụ sơ tán hay chỉ cần thông gió) mà không hoảng loạn vô ích**. |
| 5 | Là **kỹ thuật viên BQL**, tôi muốn **xem lại log đầy đủ của một sự cố đã xảy ra (dữ liệu, suy luận, ai duyệt)**, để **truy vết trách nhiệm và cải thiện ngưỡng cảnh báo sau này**. |

---

## 3. Luồng chính (5 bước)

```
Bước 1: CẢM BIẾN GỬI DỮ LIỆU
  MQTT simulator → publish liên tục 4 loại cảm biến (khói, gas, nhiệt, nước) theo khu/phòng
       ↓
Bước 2: PHÁT HIỆN BẤT THƯỜNG
  Isolation Forest (baseline riêng từng khu) + rule-threshold (ngưỡng vật lý cứng) chạy song song
       ↓
Bước 3: GHÉP DẤU HIỆU & ĐÁNH GIÁ MỨC NGUY HIỂM
  Nếu ≥2 cảm biến cùng khu bất thường trong cùng khung thời gian ngắn → LLM suy luận tương quan
  → Gán 1 trong 4 mức: Thấp / Trung bình / Cao / Khẩn cấp
       ↓
Bước 4: GỬI CẢNH BÁO KÈM HƯỚNG DẪN
  Mức Trung bình trở lên → thông báo app/email cho Cư dân (hướng dẫn xử lý) + BQL (đề xuất hành động)
       ↓
Bước 5: NGƯỜI QUẢN LÝ DUYỆT HÀNH ĐỘNG (HITL)
  BQL xem dữ liệu gốc + lý do → Duyệt/Từ chối → qua Safety Invariant Checker (rule xác định) → Actuator mô phỏng
  Ngoại lệ: vượt ngưỡng nguy hiểm tính mạng đã định trước → tự động kích hoạt tối thiểu, có log, vẫn báo BQL song song
```

---

## 4. Yêu cầu chức năng

### 4.1 Phải có (bắt buộc cho demo)
- Thu dữ liệu từ ≥ 4 loại cảm biến mô phỏng qua MQTT, lưu TimescaleDB.
- Phát hiện bất thường bằng Isolation Forest (baseline/khu) + rule-threshold độc lập.
- Tương quan ≥ 2 cảm biến cho 2 kịch bản: cháy (nhiệt+khói), rò gas (gas+nhiệt).
- Phân 4 mức nguy hiểm, cảnh báo đa kênh (app + email/push giả lập).
- Safety Invariant Checker (chặn lệnh xung đột, chặn vòng lặp bật-tắt vô hạn) — có unit test.
- HITL bắt buộc cho lệnh vật lý, có timeout + fallback không tự thực thi (trừ ngoại lệ khẩn cấp).
- Dashboard 2 vai trò (Cư dân xem khu mình / BQL xem toàn bộ + duyệt HITL).
- Log sự cố đầy đủ, không sửa được sau khi ghi.

### 4.2 Nên có (nếu còn thời gian sau khi Phải có đã chạy ổn)
- Học lại baseline định kỳ để thích nghi pattern mới của từng khu.
- Mini chart xu hướng cảm biến theo thời gian trên dashboard BQL.
- Xử lý tương quan thêm cho ngập nước (ví dụ nước + điện áp bất thường).

### 4.3 Không làm (ngoài phạm vi dự án này)
- Không điều khiển thiết bị vật lý thật — chỉ actuator mô phỏng.
- Không mô phỏng lan truyền sự cố không gian hay gợi ý lộ trình sơ tán.
- Không dùng LSTM hay bộ dữ liệu real-world (Building Data Genome, UK-DALE...).
- Không có báo cáo tự động sinh văn bản sau sự cố.
- Không có thuật toán tối ưu đa mục tiêu học thuật — ưu tiên an toàn > tiện nghi > năng lượng được hard-code đơn giản trong Safety Checker.

---

## 5. Ràng buộc (lấy từ ràng buộc gốc của đề)

| Ràng buộc | Chi tiết áp dụng |
|---|---|
| **Bắt buộc người duyệt (HITL)** | Mọi lệnh vật lý (đóng van gas/nước, ngắt điện, kích chuông toàn khu) phải chờ BQL duyệt, **trừ** khi vượt ngưỡng nguy hiểm tính mạng đã định trước (ví dụ gas ≥ ngưỡng nổ) — khi đó tự động kích hoạt hành động an toàn tối thiểu, có log, đồng thời vẫn gửi yêu cầu HITL cho hành động tiếp theo |
| **Bảo mật dữ liệu** | Dữ liệu cảm biến & vị trí căn hộ không lộ cho vai trò không có quyền — Cư dân chỉ xem được khu mình, kiểm tra bằng test phân quyền API |
| **Độ trễ** | Độ trễ cực thấp cho sự cố an toàn tính mạng — đo bằng số liệu thật trên môi trường demo (không đặt số mục tiêu tùy ý nếu chưa test), báo cáo trung bình + p95 |
| **Độ chính xác & độ nhạy cân bằng** | Không được bỏ sót (recall thấp) lẫn không được báo nhiễu (precision thấp) — phải có số liệu confusion matrix cụ thể, không dùng mô tả chung chung |
| **Lớp kiểm tra bất biến an toàn xác định** | Mọi lệnh điều khiển phải qua Safety Invariant Checker (rule-based, KHÔNG dùng LLM) trước khi thực thi trên môi trường mô phỏng — chống xung đột lệnh và vòng lặp bật-tắt vô hạn |
| **Chi phí** | Dự án chạy bằng dữ liệu giả lập + LLM API — nhóm cần tự theo dõi chi phí gọi API thực tế trong quá trình dev (số liệu giá/tốc độ model thay đổi theo thời gian, không chốt cứng trong PRD này) |

---

## 6. Dữ liệu

**Nguồn:** Dữ liệu **hoàn toàn giả lập**, sinh bởi MQTT publisher script tự viết (không dùng dữ liệu cảm biến thật, không có thiết bị vật lý).

**Quy tắc giả lập:**
| Loại kịch bản | Cách sinh |
|---|---|
| **Bình thường (baseline)** | Dao động quanh giá trị trung bình theo khu, có chu kỳ theo giờ trong ngày (ví dụ nhiệt độ phòng dao động 24-28°C ban ngày, thấp hơn ban đêm) + nhiễu ngẫu nhiên nhỏ (Gaussian noise) |
| **Anomaly đơn lẻ** | 1 cảm biến tăng/giảm đột biến ngoài baseline, không kèm cảm biến khác — dùng để test rule-threshold và false positive |
| **Anomaly tương quan — Cháy** | Nhiệt tăng dần + khói tăng đồng thời trong cùng khu, trong cửa sổ thời gian ngắn (nhóm định nghĩa, ví dụ 60 giây) |
| **Anomaly tương quan — Rò gas** | Gas tăng (% LEL) + nhiệt tăng nhẹ cùng khu |
| **Mất kết nối cục bộ** | Dừng publish 1 cảm biến > 30 giây để test xử lý `sensor_status: offline` |

⚠️ Ngưỡng số liệu cụ thể (% LEL của gas, °C ngưỡng nhiệt) dùng để sinh dữ liệu giả lập là **giá trị khởi điểm nhóm tự đặt để code và test**, không phải số liệu đã kiểm chứng từ datasheet cảm biến thật.

---

## 7. Cách đo

*Đo trên bộ kịch bản mô phỏng tự tạo (mục 6), không phải dữ liệu production — vì sản phẩm chạy hoàn toàn trên môi trường giả lập trong 5 tuần.*

| Đo gì | Đo bằng bộ dữ liệu nào | Mục tiêu |
|---|---|---|
| Tỷ lệ bắt đúng sự cố đã inject (recall) | Tập test ≥ 20 kịch bản/loại (cháy, rò gas) đã inject có kiểm soát | ≥ 90% |
| Báo động nhầm (false positive) | 24h dữ liệu baseline bình thường, không inject anomaly | ≤ 1 lần/ngày mô phỏng |
| Thời gian từ anomaly xảy ra đến cảnh báo hiển thị | Chênh lệch timestamp log, ≥ 20 lần đo | Trung bình ≤ 3 giây (môi trường local/demo) |
| An toàn Safety Checker | Unit test riêng cho chống xung đột lệnh + chống vòng lặp bật-tắt | 100% test case phải pass trước khi merge |

---

## 8. Giả định và rủi ro

**Giả định:**
- Agent xử lý thật dữ liệu MQTT do simulator sinh ra (không hard-code sẵn output cho 1 kịch bản demo); "user" ở đây là người thao tác dashboard (xem cảnh báo, duyệt HITL) — là người thật, không phải script giả lập click.
- Deploy lên 1 server/cloud thật có URL truy cập công khai (ví dụ VPS hoặc free-tier cloud).
- 5 người đóng vai kỹ thuật viên BQL (người dùng chính đã chốt ở Brief mục 2) thao tác trực tiếp trên dashboard với dữ liệu cảm biến giả lập đang chạy — không phải lắp cảm biến thật vào tòa nhà thật.

**Rủi ro:**

| Rủi ro | Mức độ | Giảm thiểu |
|---|---|---|
| G2 yêu cầu ≥10 PR merged + video demo + architecture diagram + eval 5 test case — khối lượng tài liệu hóa lớn | Cao | Làm song song: mỗi PR nhỏ (theo module ở mục 9) merge ngay khi xong, không gộp PR lớn cuối kỳ; viết sẵn khung README/diagram từ đầu tuần, điền dần |
| Tìm được ≥5 người đóng vai BQL thật để pilot trong khoảng 1 tuần | Cao | Liên hệ người pilot **ngay sau G2** (không chờ đến gần hạn G3), có thể là sinh viên khác lớp/ngành đóng vai, miễn có hướng dẫn ngữ cảnh đầy đủ trước khi họ dùng |
| Deploy "production URL" cần hạ tầng ngoài Docker Compose local | Trung bình | Chọn giải pháp deploy đơn giản nhất đủ dùng (ví dụ 1 VPS chạy Docker Compose, hoặc PaaS free-tier), không tự ý nâng cấp hạ tầng phức tạp nếu không cần thiết cho mục tiêu "có URL truy cập được" |
| Evaluation Metrics + Cost & Performance report (G3) cần số liệu đo thật trên hệ thống đã chạy — nếu Isolation Forest/Correlation chưa ổn định ở G2 thì G3 không có dữ liệu sạch để đo | Trung bình | Phải hoàn thành đo thử nghiệm sơ bộ (mục 7) ngay trong giai đoạn G2→G3, không dồn hết việc đo vào những ngày cuối trước hạn G3 |

---

## 9. Kế hoạch (bắt đầu 13/11)

### G2 — 22/11 (9 ngày): MVP — agent xử lý thật, giải quyết được 1 user flow chính, chưa cần tối ưu

**Mục tiêu MVP:** Chọn **user flow chính = Tình huống 1 (mục 2)** — phát hiện tương quan nhiệt+khói (cháy) cho 1 khu, hiển thị cảnh báo thật trên dashboard, kỹ thuật viên (thật) xem được và duyệt HITL. Đây là 1 luồng đủ để "chứng minh có giải quyết vấn đề" mà không cần làm cả 4 cảm biến + 2 kịch bản tương quan hoàn chỉnh.

**Việc kỹ thuật cần làm:**
- [ ] MQTT simulator sinh dữ liệu khói + nhiệt (tối thiểu, ưu tiên 2 cảm biến của user flow chính), có kịch bản baseline + anomaly tương quan cháy (mục 6).
- [ ] Ingest Node nhận dữ liệu thật từ MQTT, ghi vào TimescaleDB — **không hard-code output mẫu**.
- [ ] Rule-threshold + Correlation Node (LLM) chạy thật trên dữ liệu vừa nhận, sinh cảnh báo + lý do suy luận thật (không phải câu trả lời cố định soạn sẵn).
- [ ] Safety Invariant Checker có khung rule tối thiểu (chặn xung đột lệnh cơ bản).
- [ ] FastAPI backend expose API thật cho dữ liệu cảm biến + cảnh báo + HITL.
- [ ] Dashboard React: màn hình BQL tối thiểu — xem cảnh báo thật + modal HITL (duyệt/từ chối) thao tác được bằng tay thật (không phải demo giả lập click).

### G3 — 29/11 (7 ngày): Production ready — đo được chất lượng, an toàn, ổn định, pilot người dùng thật

**Mở rộng từ MVP G2:** thêm cảm biến gas + nước (đủ 4 loại), thêm kịch bản rò gas (kịch bản tương quan thứ 2), hoàn thiện phân quyền 2 vai trò, hoàn thiện Safety Checker.

**Việc kỹ thuật cần làm:**
- [ ] Thêm cảm biến gas + nước vào simulator; Isolation Forest train baseline đủ 4 loại/khu, thay thế dần rule-threshold đơn giản ở G2.
- [ ] Correlation Node mở rộng sang kịch bản rò gas (gas+nhiệt), bên cạnh cháy đã có ở G2.
- [ ] Safety Invariant Checker hoàn thiện: thêm chặn vòng lặp bật-tắt vô hạn (oscillation) — viết unit test, phải pass 100% trước khi deploy.
- [ ] Dashboard hoàn thiện phân quyền đầy đủ: Cư dân chỉ xem khu mình, BQL xem toàn bộ (theo Wireframe).
- [ ] Log sự cố đầy đủ, immutable, có thể truy xuất lại cho mục Reliability bên dưới.
- [ ] Deploy lên server/cloud thật, có URL truy cập công khai (xem giả định mục 8).

---

**Tài liệu liên quan:** `01_Brief_v2.md` (căn cứ).