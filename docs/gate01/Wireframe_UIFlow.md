# WIREFRAME / UI FLOW v2 — SC-04: SentinelIoT
*AI Agent Phát Hiện Bất Thường Cảm Biến IoT (Rò Gas, Cháy, Ngập Nước)*

---

## Danh sách 4 màn hình chính

| # | Màn hình | Vai trò | Vai trò trong luồng |
|---|---|---|---|
| 1 | Tổng quan cảm biến theo căn hộ | Cư dân | Điểm vào, xem trạng thái 4 cảm biến khu mình |
| 2 | Chi tiết một cảnh báo | Cư dân (xem) → BQL (nhận yêu cầu) | Hiển thị dấu hiệu, mức nguy hiểm, hướng dẫn xử lý |
| 3 | Duyệt hành động (HITL) | Kỹ thuật BQL | Duyệt/từ chối lệnh vật lý, có dữ liệu gốc + lý do |
| 4 | Lịch sử sự cố | Kỹ thuật BQL | Tra cứu log đã xử lý, truy vết trách nhiệm |

---

## Màn hình 1 — Tổng quan cảm biến theo căn hộ (Cư dân)

```svg
<svg width="100%" viewBox="0 0 680 520" xmlns="http://www.w3.org/2000/svg">
<rect x="20" y="20" width="640" height="480" rx="10" fill="#ffffff" stroke="#888780" stroke-width="0.5"/>
<rect x="20" y="20" width="640" height="48" rx="10" fill="#F1EFE8" stroke="#888780" stroke-width="0.5"/>
<text x="44" y="48" font-family="sans-serif" font-size="14" font-weight="500" fill="#2C2C2A">SentinelIoT</text>
<text x="596" y="48" text-anchor="end" font-family="sans-serif" font-size="12" fill="#5F5E5A">Căn hộ A-204</text>

<rect x="40" y="86" width="600" height="44" rx="8" fill="#FAEEDA" stroke="#BA7517" stroke-width="0.5"/>
<text x="60" y="113" font-family="sans-serif" font-size="14" font-weight="500" fill="#412402">Trạng thái khu: Trung bình</text>
<text x="620" y="113" text-anchor="end" font-family="sans-serif" font-size="12" fill="#854F0B">Cập nhật realtime</text>

<rect x="40" y="148" width="280" height="76" rx="8" fill="#E6F1FB" stroke="#185FA5" stroke-width="0.5"/>
<text x="60" y="177" font-family="sans-serif" font-size="14" font-weight="500" fill="#042C53">Khói</text>
<text x="60" y="201" font-family="sans-serif" font-size="12" fill="#0C447C">12 ppm — ổn định</text>

<rect x="360" y="148" width="280" height="76" rx="8" fill="#E6F1FB" stroke="#185FA5" stroke-width="0.5"/>
<text x="380" y="177" font-family="sans-serif" font-size="14" font-weight="500" fill="#042C53">Gas</text>
<text x="380" y="201" font-family="sans-serif" font-size="12" fill="#0C447C">3% LEL — bình thường</text>

<rect x="40" y="240" width="280" height="76" rx="8" fill="#FAECE7" stroke="#993C1D" stroke-width="0.5"/>
<text x="60" y="269" font-family="sans-serif" font-size="14" font-weight="500" fill="#4A1B0C">Nhiệt độ</text>
<text x="60" y="293" font-family="sans-serif" font-size="12" fill="#712B13">38°C — đang tăng</text>

<rect x="360" y="240" width="280" height="76" rx="8" fill="#E6F1FB" stroke="#185FA5" stroke-width="0.5"/>
<text x="380" y="269" font-family="sans-serif" font-size="14" font-weight="500" fill="#042C53">Ngập nước</text>
<text x="380" y="293" font-family="sans-serif" font-size="12" fill="#0C447C">0 cm — bình thường</text>

<rect x="40" y="340" width="600" height="60" rx="8" fill="#FAEEDA" stroke="#BA7517" stroke-width="0.5"/>
<text x="60" y="365" font-family="sans-serif" font-size="14" font-weight="500" fill="#412402">Cảnh báo gần nhất: Nhiệt + khói tăng cùng lúc</text>
<text x="60" y="387" font-family="sans-serif" font-size="12" fill="#854F0B">Nhấn để xem hướng dẫn xử lý →</text>

<rect x="40" y="420" width="600" height="64" rx="8" fill="#ffffff" stroke="#888780" stroke-width="0.5"/>
<text x="60" y="444" font-family="sans-serif" font-size="14" font-weight="500" fill="#2C2C2A">Lịch sử cảnh báo khu mình</text>
<text x="60" y="466" font-family="sans-serif" font-size="12" fill="#5F5E5A">10:02 Trung bình · 09:40 Thấp · Hôm qua 22:15 Thấp</text>
</svg>
```

**Mô tả khối:** Header tĩnh → Banner trạng thái tổng quan (màu theo mức nguy hiểm) → 4 thẻ cảm biến (khói/gas/nhiệt/nước) → Banner cảnh báo gần nhất (bấm vào để sang Màn hình 2) → Lịch sử ngắn gọn (chỉ đọc).

---

## Màn hình 2 — Chi tiết một cảnh báo

```svg
<svg width="100%" viewBox="0 0 680 460" xmlns="http://www.w3.org/2000/svg">
<rect x="20" y="20" width="640" height="420" rx="10" fill="#ffffff" stroke="#888780" stroke-width="0.5"/>
<rect x="20" y="20" width="640" height="48" rx="10" fill="#F1EFE8" stroke="#888780" stroke-width="0.5"/>
<text x="44" y="48" font-family="sans-serif" font-size="12" fill="#5F5E5A">← Quay lại</text>
<text x="340" y="48" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="500" fill="#2C2C2A">Chi tiết cảnh báo</text>

<rect x="40" y="86" width="600" height="46" rx="8" fill="#FAECE7" stroke="#993C1D" stroke-width="0.5"/>
<text x="60" y="113" font-family="sans-serif" font-size="14" font-weight="500" fill="#4A1B0C">Mức nguy hiểm: CAO</text>

<rect x="40" y="148" width="600" height="92" rx="8" fill="#ffffff" stroke="#888780" stroke-width="0.5"/>
<text x="60" y="176" font-family="sans-serif" font-size="14" font-weight="500" fill="#2C2C2A">Dấu hiệu phát hiện</text>
<text x="60" y="200" font-family="sans-serif" font-size="12" fill="#5F5E5A">Nhiệt độ: 52°C (tăng 8°C/phút)</text>
<text x="60" y="220" font-family="sans-serif" font-size="12" fill="#5F5E5A">Khói: 38 ppm (gấp 3 lần mức bình thường của khu)</text>

<rect x="40" y="256" width="600" height="92" rx="8" fill="#FAEEDA" stroke="#BA7517" stroke-width="0.5"/>
<text x="60" y="284" font-family="sans-serif" font-size="14" font-weight="500" fill="#412402">Lý do: nguy cơ cháy tại khu A-204</text>
<text x="60" y="308" font-family="sans-serif" font-size="12" fill="#854F0B">Nhiệt và khói cùng tăng trong 60 giây gần nhất</text>
<text x="60" y="328" font-family="sans-serif" font-size="12" fill="#854F0B">tại cùng khu vực.</text>

<rect x="40" y="364" width="600" height="56" rx="8" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.5"/>
<text x="60" y="390" font-family="sans-serif" font-size="14" font-weight="500" fill="#04342C">Hướng dẫn: rời khu vực, không dùng thang máy</text>
<text x="60" y="410" font-family="sans-serif" font-size="12" fill="#085041">Nhấn để xem hướng dẫn đầy đủ →</text>
</svg>
```

**Mô tả khối:** Banner mức nguy hiểm (màu theo mức) → Khối "Dấu hiệu phát hiện" (dữ liệu số thô từ cảm biến) → Khối "Lý do" (kết quả suy luận tương quan từ LLM, PRD FR-3) → Khối "Hướng dẫn xử lý" (sinh từ LLM, ngôn ngữ tiếng Việt dễ hiểu).

---

## Màn hình 3 — Duyệt hành động (HITL, Kỹ thuật BQL)

```svg
<svg width="100%" viewBox="0 0 680 500" xmlns="http://www.w3.org/2000/svg">
<rect x="20" y="20" width="640" height="460" rx="10" fill="#ffffff" stroke="#888780" stroke-width="0.5"/>
<rect x="20" y="20" width="640" height="48" rx="10" fill="#F1EFE8" stroke="#888780" stroke-width="0.5"/>
<text x="44" y="48" font-family="sans-serif" font-size="14" font-weight="500" fill="#2C2C2A">Xác nhận hành động vật lý</text>
<text x="596" y="48" text-anchor="end" font-family="sans-serif" font-size="12" fill="#5F5E5A">Kỹ thuật BQL</text>

<rect x="40" y="86" width="600" height="40" rx="8" fill="#FCEBEB" stroke="#A32D2D" stroke-width="0.5"/>
<text x="60" y="110" font-family="sans-serif" font-size="14" font-weight="500" fill="#501313">Mức nguy hiểm: CAO — Tầng 2, Khu A-204</text>

<rect x="40" y="142" width="600" height="92" rx="8" fill="#ffffff" stroke="#888780" stroke-width="0.5"/>
<text x="60" y="170" font-family="sans-serif" font-size="14" font-weight="500" fill="#2C2C2A">Dữ liệu gốc</text>
<text x="60" y="194" font-family="sans-serif" font-size="12" fill="#5F5E5A">Nhiệt = 52°C (ngưỡng 50°C) | Khói = 38 ppm (baseline 12 ppm)</text>
<text x="60" y="214" font-family="sans-serif" font-size="12" fill="#5F5E5A">Nguồn: cảm biến TEMP-204, SMOKE-204</text>

<rect x="40" y="250" width="600" height="68" rx="8" fill="#FAEEDA" stroke="#BA7517" stroke-width="0.5"/>
<text x="60" y="276" font-family="sans-serif" font-size="14" font-weight="500" fill="#412402">Lý do suy luận</text>
<text x="60" y="298" font-family="sans-serif" font-size="12" fill="#854F0B">Nhiệt tăng 8°C/phút kèm khói tăng 3 lần baseline → nguy cơ cháy cao</text>

<rect x="40" y="334" width="600" height="56" rx="8" fill="#ffffff" stroke="#888780" stroke-width="0.5"/>
<text x="60" y="360" font-family="sans-serif" font-size="14" font-weight="500" fill="#2C2C2A">Hành động đề xuất: kích chuông khu A-204 + đóng van gas tầng 2</text>
<text x="60" y="380" font-family="sans-serif" font-size="12" fill="#5F5E5A">Thời gian còn lại để xác nhận: 02:00</text>

<rect x="40" y="406" width="290" height="54" rx="8" fill="#EAF3DE" stroke="#3B6D11" stroke-width="0.5"/>
<text x="185" y="438" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="500" fill="#173404">Duyệt</text>

<rect x="350" y="406" width="290" height="54" rx="8" fill="#FCEBEB" stroke="#A32D2D" stroke-width="0.5"/>
<text x="495" y="438" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="500" fill="#501313">Từ chối + nhập lý do</text>
</svg>
```

**Mô tả khối:** Banner mức + vị trí → Dữ liệu gốc (bắt buộc hiển thị, không được giấu) → Lý do suy luận → Hành động đề xuất + đồng hồ đếm ngược timeout → 2 nút Duyệt/Từ chối (không có nút "duyệt hàng loạt" — nguyên tắc an toàn từ PRD FR-5).

---

## Màn hình 4 — Lịch sử sự cố (Kỹ thuật BQL)

```svg
<svg width="100%" viewBox="0 0 680 420" xmlns="http://www.w3.org/2000/svg">
<rect x="20" y="20" width="640" height="380" rx="10" fill="#ffffff" stroke="#888780" stroke-width="0.5"/>
<rect x="20" y="20" width="640" height="48" rx="10" fill="#F1EFE8" stroke="#888780" stroke-width="0.5"/>
<text x="44" y="48" font-family="sans-serif" font-size="14" font-weight="500" fill="#2C2C2A">Lịch sử sự cố</text>
<text x="596" y="48" text-anchor="end" font-family="sans-serif" font-size="12" fill="#5F5E5A">Lọc ▾</text>

<rect x="40" y="84" width="600" height="32" fill="#F1EFE8" stroke="#888780" stroke-width="0.5"/>
<text x="56" y="104" font-family="sans-serif" font-size="12" fill="#5F5E5A">Thời gian</text>
<text x="196" y="104" font-family="sans-serif" font-size="12" fill="#5F5E5A">Khu</text>
<text x="296" y="104" font-family="sans-serif" font-size="12" fill="#5F5E5A">Mức</text>
<text x="396" y="104" font-family="sans-serif" font-size="12" fill="#5F5E5A">Lý do</text>
<text x="560" y="104" font-family="sans-serif" font-size="12" fill="#5F5E5A">Trạng thái</text>

<rect x="40" y="116" width="600" height="40" fill="#ffffff" stroke="#888780" stroke-width="0.5"/>
<text x="56" y="140" font-family="sans-serif" font-size="12" fill="#2C2C2A">Hôm nay 10:02</text>
<text x="196" y="140" font-family="sans-serif" font-size="12" fill="#2C2C2A">A-204</text>
<text x="296" y="140" font-family="sans-serif" font-size="12" fill="#2C2C2A">Cao</text>
<text x="396" y="140" font-family="sans-serif" font-size="12" fill="#2C2C2A">Nhiệt+khói</text>
<text x="560" y="140" font-family="sans-serif" font-size="12" fill="#2C2C2A">Đã duyệt</text>

<rect x="40" y="156" width="600" height="40" fill="#F1EFE8" stroke="#888780" stroke-width="0.5"/>
<text x="56" y="180" font-family="sans-serif" font-size="12" fill="#2C2C2A">Hôm nay 09:40</text>
<text x="196" y="180" font-family="sans-serif" font-size="12" fill="#2C2C2A">B-110</text>
<text x="296" y="180" font-family="sans-serif" font-size="12" fill="#2C2C2A">Trung bình</text>
<text x="396" y="180" font-family="sans-serif" font-size="12" fill="#2C2C2A">Gas vượt ngưỡng</text>
<text x="560" y="180" font-family="sans-serif" font-size="12" fill="#2C2C2A">Đã xem</text>

<rect x="40" y="196" width="600" height="40" fill="#ffffff" stroke="#888780" stroke-width="0.5"/>
<text x="56" y="220" font-family="sans-serif" font-size="12" fill="#2C2C2A">Hôm qua 22:15</text>
<text x="196" y="220" font-family="sans-serif" font-size="12" fill="#2C2C2A">A-204</text>
<text x="296" y="220" font-family="sans-serif" font-size="12" fill="#2C2C2A">Thấp</text>
<text x="396" y="220" font-family="sans-serif" font-size="12" fill="#2C2C2A">Nhiệt dao động</text>
<text x="560" y="220" font-family="sans-serif" font-size="12" fill="#2C2C2A">Đã xem</text>

<rect x="40" y="236" width="600" height="40" fill="#FCEBEB" stroke="#A32D2D" stroke-width="0.5"/>
<text x="56" y="260" font-family="sans-serif" font-size="12" fill="#501313">12/11 08:05</text>
<text x="196" y="260" font-family="sans-serif" font-size="12" fill="#501313">C-301</text>
<text x="296" y="260" font-family="sans-serif" font-size="12" fill="#501313">Khẩn cấp</text>
<text x="396" y="260" font-family="sans-serif" font-size="12" fill="#501313">Gas vượt ngưỡng tính mạng</text>
<text x="560" y="260" font-family="sans-serif" font-size="12" fill="#501313">Tự động</text>

<text x="340" y="304" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#5F5E5A">Nhấn vào 1 dòng để xem chi tiết: dữ liệu gốc, lý do, người duyệt, kết quả</text>
</svg>
```

**Mô tả khối:** Header + bộ lọc (theo khu/mức độ) → Bảng log, mỗi dòng bấm vào mở chi tiết đầy đủ (dữ liệu gốc, lý do, ai duyệt, kết quả) — đúng yêu cầu PRD FR-8 (log immutable, không sửa được).

---

## Sơ đồ nối 4 màn hình bằng mũi tên (UI Flow)

```svg
<svg width="100%" viewBox="0 0 680 420" xmlns="http://www.w3.org/2000/svg">
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M2 1L8 5L2 9" fill="none" stroke="#5F5E5A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</marker>
</defs>

<rect x="40" y="40" width="200" height="56" rx="8" fill="#E6F1FB" stroke="#185FA5" stroke-width="0.5"/>
<text x="140" y="64" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="500" fill="#042C53">1. Tổng quan cảm biến</text>
<text x="140" y="84" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#0C447C">Cư dân · theo căn hộ</text>

<rect x="440" y="40" width="200" height="56" rx="8" fill="#FAEEDA" stroke="#BA7517" stroke-width="0.5"/>
<text x="540" y="64" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="500" fill="#412402">2. Chi tiết cảnh báo</text>
<text x="540" y="84" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#854F0B">Dấu hiệu, mức, hướng dẫn</text>

<rect x="440" y="180" width="200" height="56" rx="8" fill="#FAECE7" stroke="#993C1D" stroke-width="0.5"/>
<text x="540" y="204" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="500" fill="#4A1B0C">3. Duyệt hành động</text>
<text x="540" y="224" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#712B13">Kỹ thuật BQL · HITL</text>

<rect x="40" y="180" width="200" height="56" rx="8" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.5"/>
<text x="140" y="204" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="500" fill="#04342C">4. Lịch sử sự cố</text>
<text x="140" y="224" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#085041">Kỹ thuật BQL</text>

<line x1="240" y1="68" x2="438" y2="68" stroke="#5F5E5A" stroke-width="1.5" marker-end="url(#arrow)"/>
<text x="339" y="56" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#5F5E5A">Nhấn vào banner cảnh báo</text>

<line x1="540" y1="96" x2="540" y2="178" stroke="#5F5E5A" stroke-width="1.5" marker-end="url(#arrow)"/>
<text x="620" y="137" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#5F5E5A">Hệ thống</text>
<text x="620" y="151" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#5F5E5A">gửi yêu cầu</text>

<path d="M440 208 L240 208" fill="none" stroke="#5F5E5A" stroke-width="1.5" marker-end="url(#arrow)"/>
<text x="340" y="260" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#5F5E5A">Sau khi duyệt/từ chối, ghi vào log</text>

<line x1="140" y1="180" x2="140" y2="98" stroke="#5F5E5A" stroke-width="1.5" stroke-dasharray="4 4" marker-end="url(#arrow)"/>
<text x="210" y="140" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#5F5E5A">Xem lại</text>

<rect x="40" y="280" width="600" height="110" rx="8" fill="#ffffff" stroke="#888780" stroke-width="0.5"/>
<text x="60" y="304" font-family="sans-serif" font-size="14" font-weight="500" fill="#2C2C2A">Chú giải luồng</text>
<text x="60" y="328" font-family="sans-serif" font-size="12" fill="#5F5E5A">Cư dân: 1 → 2 (xem cảnh báo và hướng dẫn, không điều khiển)</text>
<text x="60" y="348" font-family="sans-serif" font-size="12" fill="#5F5E5A">Kỹ thuật BQL: 2 → 3 (duyệt/từ chối hành động vật lý) → 4 (xem lại log)</text>
<text x="60" y="368" font-family="sans-serif" font-size="12" fill="#5F5E5A">Nét đứt: BQL có thể mở lại chi tiết từ dòng log bất kỳ lúc nào</text>
</svg>
```

**Diễn giải luồng (bằng lời, đi kèm sơ đồ):**
1. **Cư dân** mở Màn hình 1, thấy banner cảnh báo → nhấn vào → chuyển sang Màn hình 2 xem dấu hiệu, mức nguy hiểm, hướng dẫn xử lý.
2. Khi mức nguy hiểm cần hành động vật lý, hệ thống tự động đẩy yêu cầu sang Màn hình 3 — chỉ **Kỹ thuật BQL** nhìn thấy và xử lý màn hình này.
3. Sau khi BQL bấm Duyệt hoặc Từ chối, kết quả được ghi lại và xuất hiện ngay trong Màn hình 4 (Lịch sử sự cố).
4. BQL có thể quay lại Màn hình 4 bất kỳ lúc nào để tra cứu, và từ một dòng log mở lại được chi tiết gốc (nét đứt) — phục vụ truy vết.

---

**Ghi chú:** 2 vai trò không dùng chung màn hình 3 — Cư dân không bao giờ thấy modal HITL, đúng ràng buộc phân quyền ở PRD mục 4 (Bảo mật dữ liệu).
