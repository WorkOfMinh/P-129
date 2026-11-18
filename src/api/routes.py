"""API routes v2 — truyền thread_id cho checkpointer để HITL resume hoạt động.

Vì sao đổi: graph v2 compile với MemorySaver — invoke bắt buộc có
`config={"configurable": {"thread_id": ...}}`. Client giữ session_id,
gửi lại kèm Command(resume=...) khi user duyệt/từ chối hành động rủi ro.
"""

import logging
from datetime import UTC, datetime
from itertools import count
from pathlib import Path
from threading import Lock
from typing import Literal

from dotenv import dotenv_values
from fastapi import APIRouter, HTTPException
from httpx import RequestError
from langgraph.types import Command
from postgrest.exceptions import APIError
from pydantic import BaseModel
from supabase import create_client

from src.agents.graph import agent
from src.agents.incident_graph import build_incident_graph
from src.models.schemas import ChatRequest, ChatResponse

logger = logging.getLogger("ai20k.api")

router = APIRouter()


def _config(session_id: str) -> dict:
    return {"configurable": {"thread_id": session_id}}


def _to_chat_response(result: dict, session_id: str) -> ChatResponse:
    # Cả /chat lẫn /chat/resume đều có thể dừng ở interrupt (vd agent muốn gửi email thứ 2)
    if "__interrupt__" in result:
        interrupts = result["__interrupt__"]
        payload = getattr(interrupts[0], "value", interrupts[0])
        return ChatResponse(
            response=f"[CẦN PHÊ DUYỆT] {payload}. POST /chat/resume với resume='approve' hoặc 'reject'.",
            analysis="HITL interrupt",
            session_id=session_id,
        )
    trace = result.get("tool_trace", [])
    analysis = "; ".join(f"{t['tool']}({t['args']}) -> {str(t['output'])[:60]}" for t in trace)
    return ChatResponse(response=result.get("response", ""), analysis=analysis, session_id=session_id)


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Chat với AI agent. Nếu agent đang chờ human review, response chứa hướng dẫn resume."""
    try:
        result = await agent.ainvoke({"query": request.message}, config=_config(request.session_id))
        return _to_chat_response(result, request.session_id)
    except Exception as exc:
        logger.error("FAILED /chat — %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


class ResumeRequest(BaseModel):
    session_id: str  # bắt buộc — lấy từ ChatResponse.session_id của /chat
    resume: str  # "approve" | "reject"


@router.post("/chat/resume", response_model=ChatResponse)
async def chat_resume(request: ResumeRequest) -> ChatResponse:
    """Resume sau HITL interrupt — phê duyệt hoặc từ chối hành động rủi ro."""
    try:
        result = await agent.ainvoke(Command(resume=request.resume), config=_config(request.session_id))
        return _to_chat_response(result, request.session_id)
    except Exception as exc:
        logger.error("FAILED /chat/resume — %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/status")
async def agent_status():
    """Kiểm tra trạng thái agent."""
    return {"status": "ready", "agent": "LangGraph Agent v2.0"}

@router.get("/telemetry/moi_nhat")
def lay_telemetry_moi_nhat():
    """Đọc phép đo mới nhất của căn A101 từ Supabase cá nhân."""
    env_file = Path(__file__).resolve().parents[2] / ".env.supabase.local"
    config = dotenv_values(env_file)
    url = config.get("SUPABASE_URL")
    key = config.get("SUPABASE_KEY")

    if not url or not key:
        raise HTTPException(
            status_code=503,
            detail="Thiếu cấu hình Supabase trong .env.supabase.local",
        )

    client = create_client(url, key)

    try:
        result = (
            client.table("sensor_data_lab")
            .select(
                "can_ho,thoi_gian:timestamp_do,nhiet_do:nhiet_do_c,"
                "khoi:khoi_ppm,gas:gas_pct_lel,nuoc:muc_nuoc_cm"
            )
            .eq("can_ho", "A101")
            .order("timestamp_do", desc=True)
            .order("id", desc=True)
            .limit(1)
            .execute()
        )
    except (APIError, RequestError) as exc:
        logger.warning("Lỗi đọc telemetry A101: %s", type(exc).__name__)
        raise HTTPException(
            status_code=502,
            detail="Không đọc được dữ liệu cảm biến từ Supabase.",
        ) from exc

    return {
        "thoi_gian_cap_nhat": datetime.now(UTC),
        "du_lieu": result.data,
    }

class CanhBaoRequest(BaseModel):
    can_ho: str
    thoi_gian: str
    nhiet_do: float
    khoi: float
    trang_thai: Literal["canh_bao"]
    ly_do: str


def bat_chuong_mo_phong(state):
    print(
        f"[ACTUATOR DEMO] Bật chuông căn {state['can_ho']} "
        f"cho sự cố {state['su_kien_id']}",
        flush=True,
    )
    return {}

# Dùng chung trong một lần chạy Uvicorn local.
incident_graph = build_incident_graph(bat_chuong_mo_phong)
incident_ids = count(start=1)

danh_sach_id: list[int] = []
khoa_danh_sach = Lock()

@router.post("/su_co", status_code=201)
def tao_su_co(canh_bao: CanhBaoRequest):
    su_kien_id = next(incident_ids)
    config = {"configurable": {"thread_id": f"su-kien-{su_kien_id}"}}

    state = {
        "su_kien_id": su_kien_id,
        "can_ho": canh_bao.can_ho,
        "bang_chung": [canh_bao.model_dump()],
    }

    result = incident_graph.invoke(state, config=config)
    interrupts = result.get("__interrupt__", ())

    if not interrupts:
        raise HTTPException(
            status_code=500,
            detail="Graph chưa trả về yêu cầu BQL duyệt.",
        )
    with khoa_danh_sach:
        danh_sach_id.append(su_kien_id)

    return {
        "trang_thai": "cho_phe_duyet",
        **interrupts[0].value,
    }

@router.get("/su_co")
def lay_su_co(trang_thai: Literal["cho_phe_duyet"] = "cho_phe_duyet"):
    with khoa_danh_sach:
        cac_id = danh_sach_id.copy()

    du_lieu = []

    for su_kien_id in reversed(cac_id):
        config = {"configurable": {"thread_id": f"su-kien-{su_kien_id}"}}
        snapshot = incident_graph.get_state(config)

        if "cho_duyet" not in snapshot.next:
            continue

        for task in snapshot.tasks:
            for yeu_cau in task.interrupts:
                du_lieu.append({
                    **yeu_cau.value,
                    "trang_thai": trang_thai,
                })

    return {"du_lieu": du_lieu}

@router.post("/su_co/{su_kien_id}/tu_choi")
def tu_choi_su_co(su_kien_id: int):
    config = {"configurable": {"thread_id": f"su-kien-{su_kien_id}"}}
    snapshot = incident_graph.get_state(config)

    if not snapshot.values:
        raise HTTPException(status_code=404, detail="Không tìm thấy sự cố.")

    if "cho_duyet" not in snapshot.next:
        raise HTTPException(
            status_code=409,
            detail="Sự cố không còn chờ BQL duyệt.",
        )

    result = incident_graph.invoke(Command(resume="reject"), config=config)

    return {
        "su_kien_id": result["su_kien_id"],
        "can_ho": result["can_ho"],
        "quyet_dinh": result["quyet_dinh"],
        "bang_chung": result["bang_chung"],
    }

@router.post("/su_co/{su_kien_id}/dong_y")
def dong_y_su_co(su_kien_id: int):
    config = {"configurable": {"thread_id": f"su-kien-{su_kien_id}"}}
    snapshot = incident_graph.get_state(config)

    if not snapshot.values:
        raise HTTPException(status_code=404, detail="Không tìm thấy sự cố.")

    if "cho_duyet" not in snapshot.next:
        raise HTTPException(status_code=409, detail="Sự cố không còn chờ duyệt.")

    result = incident_graph.invoke(Command(resume="approve"), config=config)

    return {
        "su_kien_id": result["su_kien_id"],
        "can_ho": result["can_ho"],
        "quyet_dinh": result["quyet_dinh"],
        "ket_qua_thuc_thi": result["ket_qua_thuc_thi"],
        "ly_do_thuc_thi": result["ly_do_thuc_thi"],
    }
