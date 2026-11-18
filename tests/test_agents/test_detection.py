import pytest

from src.agents.detection import danh_gia_nhiet_khoi


@pytest.mark.parametrize(
    "nhiet_do, khoi, mong_doi",
    [
        (29.7, 6.2, "binh_thuong"),    # Số đo A101 đã đi qua pipeline
        (40.0, 6.2, "theo_doi"),       # Chỉ nhiệt đạt ngưỡng
        (29.7, 20.0, "theo_doi"),      # Chỉ khói đạt ngưỡng
        (40.0, 20.0, "canh_bao"),      # Cả hai vừa chạm ngưỡng
        (40.0, None, "thieu_du_lieu"), # Mất số đo khói
    ],
)
def test_danh_gia_a101(nhiet_do, khoi, mong_doi):
    ban_ghi = {
        "can_ho": "A101",
        "thoi_gian": "2026-11-17T08:37:04.281484+00:00",
        "nhiet_do": nhiet_do,
        "khoi": khoi,
    }

    ket_qua = danh_gia_nhiet_khoi(
        ban_ghi, nguong_nhiet=40.0, nguong_khoi=20.0
    )

    assert ket_qua["trang_thai"] == mong_doi
    assert ket_qua["can_ho"] == ban_ghi["can_ho"]
    assert ket_qua["thoi_gian"] == ban_ghi["thoi_gian"]
    assert ket_qua["ly_do"]