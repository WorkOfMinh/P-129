"""Phân tích bằng chứng trước khi BQL xem yêu cầu duyệt."""
import json
import logging
import os

logger = logging.getLogger(__name__)


def phan_tich_bang_chung(state):
    samples = []
    for item in state.get("bang_chung", []):
        if item.get("can_ho") == state["can_ho"]:
            samples.append({
                "thoi_gian": item.get("thoi_gian"),
                "nhiet_do": item.get("nhiet_do"),
                "khoi": item.get("khoi"),
            })

    result = {"nguon": "local", "so_mau": len(samples)}
    if not samples:
        result["nhan_dinh"] = "Chưa có số đo khớp căn hộ của sự cố."
        return {"phan_tich": result}

    last = samples[-1]
    result["nhan_dinh"] = (
        f"Mẫu cuối trong danh sách: nhiệt độ {last['nhiet_do']} °C, "
        f"khói {last['khoi']} ppm."
        if last["nhiet_do"] is not None and last["khoi"] is not None
        else "Mẫu cuối thiếu số đo nhiệt độ hoặc khói."
    )
    if len(samples) == 1:
        result["gioi_han"] = "Một mẫu chưa đủ để kết luận xu hướng."

    if os.getenv("INCIDENT_ANALYSIS_LLM") == "1":
        try:
            from src.services.llm import get_llm

            # Chỉ gửi số đo. Mã căn hộ và thời điểm vẫn ở trong backend.
            readings = [{k: s[k] for k in ("nhiet_do", "khoi")} for s in samples]
            response = get_llm("generate").invoke([
                ("system", "Viết nhận định tiếng Việt ngắn cho BQL từ số đo nhiệt độ °C "
                 "và khói ppm của mô phỏng. Chỉ mô tả bằng chứng. Không chẩn đoán "
                 "cháy, đưa lệnh điều khiển hoặc suy ra xu hướng từ một mẫu. "
                 "Không có thông tin về khoảng cách thời gian giữa các mẫu."),
                ("human", json.dumps(readings)),
            ], timeout=5)
            if isinstance(response.content, str) and response.content.strip():
                result.update(nguon="llm", nhan_dinh=response.content.strip())
        except Exception as exc:
            logger.warning("Phân tích LLM dùng dự phòng: %s", type(exc).__name__)
            result["nguon"] = "local_du_phong"

    return {"phan_tich": result}
