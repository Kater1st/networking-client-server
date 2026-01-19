"""
server.py - Networking Module (CSE 310)
Multi-Service TCP Server using newline-delimited JSON messages.

Protocol:
- Client sends one JSON object per line (ends with '\n')
- Server replies with one JSON object per line

Supported request types:
- ECHO
- SYSTEM_INFO
- FILE_QUERY
- HELP
"""

import socket
import threading
import json
import os
import platform
from datetime import datetime, timezone

HOST = "0.0.0.0"   # Listen on all network interfaces
PORT = 5050        # Port to listen on
SERVER_NAME = "Tinashe-NetServer"
DATA_FILE = "data.json"

# Track active clients (for SYSTEM_INFO)
active_clients_lock = threading.Lock()
active_clients = 0


def now_iso() -> str:
    """Return current time in ISO 8601 format with timezone."""
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def make_response(request_id: str, status: str, data: dict | None = None, error: dict | None = None) -> dict:
    """Build a protocol-compliant response object."""
    return {
        "request_id": request_id,
        "status": status,
        "data": data or {},
        "error": error
    }


def load_local_data() -> dict:
    """Load local JSON data from DATA_FILE. Return {} if file missing/invalid."""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def validate_request(obj: dict) -> tuple[bool, str]:
    """
    Validate the incoming request object.
    Returns (is_valid, error_message).
    """
    if not isinstance(obj, dict):
        return False, "Request must be a JSON object"
    if "type" not in obj or not isinstance(obj["type"], str) or not obj["type"].strip():
        return False, "Missing or invalid 'type' field"
    if "request_id" not in obj or not isinstance(obj["request_id"], str) or not obj["request_id"].strip():
        return False, "Missing or invalid 'request_id' field"
    if "payload" not in obj or not isinstance(obj["payload"], dict):
        return False, "Missing or invalid 'payload' field (must be an object)"
    return True, ""


def handle_request(req: dict) -> dict:
    """Handle a validated request and return a response dict."""
    req_type = req["type"].strip().upper()
    request_id = req["request_id"]
    payload = req["payload"]

    if req_type == "ECHO":
        if "message" not in payload or not isinstance(payload["message"], str):
            return make_response(
                request_id,
                "ERROR",
                error={"code": "BAD_REQUEST", "message": "ECHO requires payload.message (string)"}
            )
        return make_response(request_id, "OK", data={"echo": payload["message"]})

    if req_type == "SYSTEM_INFO":
        with active_clients_lock:
            count = active_clients
        return make_response(
            request_id,
            "OK",
            data={
                "server_name": SERVER_NAME,
                "server_time": now_iso(),
                "active_clients": count,
                "platform": platform.platform()
            }
        )

    if req_type == "FILE_QUERY":
        if "key" not in payload or not isinstance(payload["key"], str) or not payload["key"].strip():
            return make_response(
                request_id,
                "ERROR",
                error={"code": "BAD_REQUEST", "message": "FILE_QUERY requires payload.key (string)"}
            )

        data = load_local_data()
        key = payload["key"].strip()

        if key not in data:
            return make_response(
                request_id,
                "ERROR",
                error={"code": "NOT_FOUND", "message": f"Key '{key}' not found"}
            )

        return make_response(
            request_id,
            "OK",
            data={"key": key, "value": data[key]}
        )

    if req_type == "HELP":
        return make_response(
            request_id,
            "OK",
            data={"supported_types": ["ECHO", "SYSTEM_INFO", "FILE_QUERY", "HELP"]}
        )

    return make_response(
        request_id,
        "ERROR",
        error={"code": "UNKNOWN_TYPE", "message": f"Unknown request type: {req_type}"}
    )


def client_thread(conn: socket.socket, addr):
    """Handle one client connection."""
    global active_clients

    with active_clients_lock:
        active_clients += 1

    try:
        # Use makefile() so we can read line-by-line easily
        file_like = conn.makefile("r", encoding="utf-8", newline="\n")

        while True:
            line = file_like.readline()
            if not line:  # Client disconnected
                break

            line = line.strip()
            if not line:
                continue

            # Parse JSON
            try:
                req_obj = json.loads(line)
            except json.JSONDecodeError:
                # If JSON invalid, we can't trust request_id; send a generic response
                resp = make_response(
                    request_id="",
                    status="ERROR",
                    error={"code": "INVALID_JSON", "message": "Could not parse JSON request"}
                )
                conn.sendall((json.dumps(resp) + "\n").encode("utf-8"))
                continue

            # Validate request structure
            valid, msg = validate_request(req_obj)
            if not valid:
                request_id = req_obj.get("request_id", "") if isinstance(req_obj, dict) else ""
                resp = make_response(
                    request_id=request_id if isinstance(request_id, str) else "",
                    status="ERROR",
                    error={"code": "BAD_REQUEST", "message": msg}
                )
                conn.sendall((json.dumps(resp) + "\n").encode("utf-8"))
                continue

            # Handle request
            resp_obj = handle_request(req_obj)
            conn.sendall((json.dumps(resp_obj) + "\n").encode("utf-8"))

    except ConnectionResetError:
        # Client closed abruptly
        pass
    except Exception as ex:
        # Last resort: do not crash server thread
        try:
            resp = make_response(
                request_id="",
                status="ERROR",
                error={"code": "SERVER_ERROR", "message": f"Unexpected error: {type(ex).__name__}"}
            )
            conn.sendall((json.dumps(resp) + "\n").encode("utf-8"))
        except Exception:
            pass
    finally:
        try:
            conn.close()
        except Exception:
            pass

        with active_clients_lock:
            active_clients -= 1


def main():
    # Helpful startup message
    print(f"[STARTING] {SERVER_NAME} on {HOST}:{PORT}")
    print(f"[INFO] Using data file: {DATA_FILE} (for FILE_QUERY)")
    print("[INFO] Protocol: one JSON object per line (newline-delimited JSON)")

    # Create TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Allows quick restart of server without waiting for TIME_WAIT
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        s.bind((HOST, PORT))
        s.listen(5)

        print("[LISTENING] Server is waiting for connections...")

        while True:
            conn, addr = s.accept()
            print(f"[CONNECTED] Client from {addr}")

            t = threading.Thread(target=client_thread, args=(conn, addr), daemon=True)
            t.start()


if __name__ == "__main__":
    main()
