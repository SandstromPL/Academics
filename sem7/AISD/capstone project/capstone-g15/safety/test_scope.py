from safety.scope import check_write, gate_record

CLIENT = "data/clients/client_01.py"


def test_own_client_allowed():
    assert check_write(CLIENT, CLIENT)[0] is True
    assert check_write("./data/clients/client_01.py", CLIENT)[0] is True


def test_library_denied():
    ok, reason = check_write("data/libv/v2.py", CLIENT)
    assert ok is False and "library" in reason


def test_test_file_denied():
    assert check_write("data/clients/tests/test_client_01.py", CLIENT)[0] is False


def test_other_client_denied():
    assert check_write("data/clients/client_02.py", CLIENT)[0] is False


def test_traversal_denied():
    assert check_write("data/clients/../libv/v2.py", CLIENT)[0] is False
    assert check_write("../../etc/passwd", CLIENT)[0] is False


def test_gate_record_shape():
    rec = gate_record("data/libv/v2.py", CLIENT, "case_01")
    assert rec["type"] == "gate" and rec["decision"] == "deny"
    assert rec["resolved"] == "data/libv/v2.py"
