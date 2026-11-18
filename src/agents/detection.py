# src/agents/detection.py

def danh_gia_nhiet_khoi(ban_ghi, *, nguong_nhiet, nguong_khoi):
    nhiet_do = ban_ghi.get("nhiet_do")
    khoi = ban_ghi.get("khoi")

    ket_qua = {
        "can_ho": ban_ghi["can_ho"],
        "thoi_gian": ban_ghi["thoi_gian"],
        "nhiet_do": nhiet_do,
        "khoi": khoi,
    }

    if nhiet_do is None or khoi is None:
        return {
            **ket_qua,
            "trang_thai": "thieu_du_lieu",
            "ly_do": "Thiếu số đo nhiệt độ hoặc khói để đánh giá tương quan.",
        }

    nhiet_cao = nhiet_do >= nguong_nhiet
    khoi_cao = khoi >= nguong_khoi

    if nhiet_cao and khoi_cao:
        trang_thai = "canh_bao"
        ly_do = "Nhiệt độ và khói cùng đạt ngưỡng demo trong một bản tin."
    elif nhiet_cao or khoi_cao:
        trang_thai = "theo_doi"
        ly_do = "Chỉ một trong hai chỉ số đạt ngưỡng demo."
    else:
        trang_thai = "binh_thuong"
        ly_do = "Cả nhiệt độ và khói đều dưới ngưỡng demo."

    return {**ket_qua, "trang_thai": trang_thai, "ly_do": ly_do}