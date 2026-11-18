import json
import os
from pathlib import Path

from src.agents.detection import danh_gia_nhiet_khoi

from dotenv import load_dotenv
from paho.mqtt import subscribe
from supabase import create_client
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TOPIC = "toanha/canho/A101/telemetry"


def main():
    load_dotenv(PROJECT_ROOT / ".env.supabase.local")
    url = os.getenv("SUPABASE_URL")
    write_key = os.getenv("SUPABASE_WRITE_KEY")

    if not url or not write_key:
        raise SystemExit(
            "Thiếu SUPABASE_URL hoặc SUPABASE_WRITE_KEY trong .env.supabase.local"
        )

    db = create_client(url, write_key)

    print(f"Đang chờ bản tin mới trên {TOPIC} ...", flush=True)
    message = subscribe.simple(
        TOPIC,
        hostname="127.0.0.1",
        port=1883,
        qos=1,
        retained=False,
    )
    reading = json.loads(message.payload.decode("utf-8-sig"))

    if reading["can_ho"] != "A101":
        raise ValueError("Mã căn hộ trong bản tin không khớp với topic A101.")

    row = {
        "can_ho": reading["can_ho"],
        "timestamp_do": reading["thoi_gian"],
        "nhiet_do_c": reading["nhiet_do"],
        "khoi_ppm": reading["khoi"],
        "gas_pct_lel": reading["gas"],
        "muc_nuoc_cm": reading["nuoc"],
    }

    print("Đã nhận MQTT:", json.dumps(row, ensure_ascii=False))
    db.table("sensor_data_lab").insert(row).execute()
    print(f"Đã ghi Supabase: {row['can_ho']} | {row['timestamp_do']}")
    ket_qua = danh_gia_nhiet_khoi(
        reading,
        nguong_nhiet=40.0,
        nguong_khoi=20.0,
    )
    print("Kết quả đánh giá:", json.dumps(ket_qua, ensure_ascii=False))
    if ket_qua["trang_thai"] != "canh_bao":
        print("Đã lưu số đo. Trạng thái này không tạo sự cố.")
        return

    request = Request(
        "http://127.0.0.1:8000/api/v1/su_co",
        data=json.dumps(ket_qua, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=10) as response:
            su_co = json.load(response)
    except HTTPError as exc:
        raise SystemExit(f"Đã lưu số đo. API tạo sự cố trả HTTP {exc.code}.")
    except (URLError, TimeoutError) as exc:
        raise SystemExit(
            f"Đã lưu số đo. Chưa xác nhận được việc tạo sự cố: {exc}"
        )

    print(
        f"Sự cố {su_co['su_kien_id']} | "
        f"căn {su_co['can_ho']} | {su_co['trang_thai']}"
    )


if __name__ == "__main__":
    main()