from context_governor.core import (
    build_anchor_request,
    compute_density,
    process_anchors,
    should_halt,
)


def test_density_edges():
    assert compute_density("") == 0.0
    assert compute_density("alpha beta gamma") == 1.0
    assert compute_density("alpha alpha alpha") < 1.0


def test_deficit_threshold_behavior():
    assert should_halt(0.649999)
    assert not should_halt(0.65)


def test_anchor_request_format():
    payload = build_anchor_request(["a.py", "a.py", "b.py"])
    assert payload["status"] == "ANCHOR_REQUEST"
    assert payload["missing_anchors"] == ["a.py", "b.py"]
    assert payload["delimiters"]["code"] == "[CODE_SNIPPET]"


def test_process_anchors():
    parsed = process_anchors("[CODE_SNIPPET] a.py\nprint(1)\n[CONTEXT_PREV]\nold.py\n[CONTEXT_NEXT]\nnext.py")
    assert parsed["files"]["a.py"] == "print(1)"
    assert parsed["previous"] == ["old.py"]
    assert parsed["next"] == ["next.py"]
