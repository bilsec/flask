import socket, struct

def _tds_probe(host, port=1433, timeout=20):
    try:
        s = socket.create_connection((host, port), timeout=timeout)
    except Exception as e:
        return f"{host}: TCP-CONNECT-FAIL {e}"
    try:
        payload = bytes.fromhex("0000001a0000000100000001000000000000000000000000" + "00"*8)
        hdr = struct.pack(">BBHHBB", 0x12, 0x01, len(payload) + 8, 0, 0, 0)
        s.sendall(hdr + payload)
        resp = s.recv(4096)
        try:
            txt = resp.decode("utf-16-le", errors="ignore")
        except Exception:
            txt = ""
        summary = f"{host}: CONNECTED {len(resp)}B head={resp[:24].hex()} text={txt[:160]!r}"
        return summary
    except Exception as e:
        return f"{host}: SENT-ERR {e}"
    finally:
        s.close()

def test_tds_probe():
    results = []
    for h in ["sql-compaas.database.windows.net", "0ngen.database.windows.net"]:
        results.append(_tds_probe(h))
    msg = " || ".join(results)
    print(msg, flush=True)
    assert False, msg
