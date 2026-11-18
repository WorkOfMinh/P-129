from typing import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt

from src.agents.evidence_analysis import phan_tich_bang_chung


class IncidentState(TypedDict, total=False):
    su_kien_id: int
    can_ho: str
    bang_chung: list[dict]
    quyet_dinh: str
    ket_qua_thuc_thi: str
    ly_do_thuc_thi: str
    phan_tich: dict


def review(state: IncidentState) -> dict:
    """Dừng graph để BQL xem bằng chứng và duyệt hoặc từ chối."""
    decision = interrupt({
        "su_kien_id": state["su_kien_id"],
        "can_ho": state["can_ho"],
        "bang_chung": state["bang_chung"],
        "phan_tich": state["phan_tich"],
        "de_xuat": "kich_chuong_mo_phong",
    })

    if decision not in ("approve", "reject"):
        raise ValueError("Quyết định phải là approve hoặc reject")

    return {"quyet_dinh": decision}


def build_incident_graph(actuator):
    from threading import Lock

    # Trạng thái mô phỏng dùng chung giữa các sự cố trong cùng graph.
    chuong_dang_bat: set[str] = set()
    khoa_chuong = Lock()

    def kiem_tra_va_bat_chuong(state: IncidentState) -> dict:
        can_ho = state["can_ho"]

        with khoa_chuong:
            if can_ho in chuong_dang_bat:
                return {
                    "ket_qua_thuc_thi": "bo_qua",
                    "ly_do_thuc_thi": f"Chuông mô phỏng của {can_ho} đã bật.",
                }

            actuator(state)
            chuong_dang_bat.add(can_ho)
            return {
                "ket_qua_thuc_thi": "da_thuc_thi",
                "ly_do_thuc_thi": f"Đã bật chuông mô phỏng của {can_ho}.",
            }

    builder = StateGraph(IncidentState)
    builder.add_node("phan_tich_bang_chung", phan_tich_bang_chung)
    builder.add_node("cho_duyet", review)
    builder.add_node("kiem_tra_va_bat_chuong", kiem_tra_va_bat_chuong)

    builder.add_edge(START, "phan_tich_bang_chung")
    builder.add_edge("phan_tich_bang_chung", "cho_duyet")
    builder.add_conditional_edges(
        "cho_duyet",
        lambda state: state["quyet_dinh"],
        {
            "reject": END,
            "approve": "kiem_tra_va_bat_chuong",
        },
    )
    builder.add_edge("kiem_tra_va_bat_chuong", END)

    return builder.compile(checkpointer=MemorySaver())
