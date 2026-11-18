from unittest.mock import Mock

from langgraph.types import Command

from src.agents.incident_graph import build_incident_graph


def test_a101_reject_preserves_evidence_and_skips_actuator():
    evidence = [
        {
            "can_ho": "A101",
            "thoi_gian": "2026-11-15T09:59:57Z",
            "nhiet_do": 28.1,
            "khoi": 6.2,
            "gas": 0.9,
            "nuoc": 0.5,
            "nguon": "mo_phong",
        },
        {
            "can_ho": "A101",
            "thoi_gian": "2026-11-15T10:00:00Z",
            "nhiet_do": 35.0,
            "khoi": 18.0,
            "gas": 0.9,
            "nuoc": 0.5,
            "nguon": "mo_phong",
        },
    ]

    actuator = Mock(return_value={})
    graph = build_incident_graph(actuator)
    config = {"configurable": {"thread_id": "su-kien-12"}}

    # Lần 1: graph nhận sự cố và dừng chờ BQL.
    paused = graph.invoke(
        {
            "su_kien_id": 12,
            "can_ho": "A101",
            "bang_chung": evidence,
        },
        config=config,
    )

    request = paused["__interrupt__"][0].value
    assert request["su_kien_id"] == 12
    assert request["can_ho"] == "A101"
    assert request["bang_chung"] == evidence
    actuator.assert_not_called()

    # Lần 2: BQL từ chối. Dùng cùng thread_id để tiếp tục đúng sự cố.
    graph.invoke(Command(resume="reject"), config=config)

    saved = graph.get_state(config)
    assert saved.values["su_kien_id"] == 12
    assert saved.values["quyet_dinh"] == "reject"
    assert saved.values["bang_chung"] == evidence
    assert saved.next == ()
    actuator.assert_not_called()
    
def test_a101_approve_calls_mock_actuator_once():
    evidence = [
        {
            "can_ho": "A101",
            "thoi_gian": "2026-11-15T09:59:57Z",
            "nhiet_do": 28.1,
            "khoi": 6.2,
            "gas": 0.9,
            "nuoc": 0.5,
            "nguon": "mo_phong",
        },
        {
            "can_ho": "A101",
            "thoi_gian": "2026-11-15T10:00:00Z",
            "nhiet_do": 35.0,
            "khoi": 18.0,
            "gas": 0.9,
            "nuoc": 0.5,
            "nguon": "mo_phong",
        },
    ]

    actuator = Mock(return_value={})
    graph = build_incident_graph(actuator)
    config = {"configurable": {"thread_id": "su-kien-12"}}

    # Lần 1: graph nhận sự cố và dừng chờ BQL.
    paused = graph.invoke(
        {
            "su_kien_id": 12,
            "can_ho": "A101",
            "bang_chung": evidence,
        },
        config=config,
    )

    request = paused["__interrupt__"][0].value
    assert request["su_kien_id"] == 12
    assert request["can_ho"] == "A101"
    assert request["bang_chung"] == evidence
    actuator.assert_not_called()

    graph.invoke(Command(resume="approve"), config=config)

    saved = graph.get_state(config)
    assert saved.values["quyet_dinh"] == "approve"
    assert saved.next == ()

    actuator.assert_called_once()
    state_sent_to_actuator = actuator.call_args.args[0]
    assert state_sent_to_actuator["su_kien_id"] == 12
    assert state_sent_to_actuator["can_ho"] == "A101"
    assert state_sent_to_actuator["bang_chung"] == evidence
    assert state_sent_to_actuator["quyet_dinh"] == "approve"