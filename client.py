"""
client.py
CSE 310 – Applied Programming (Networking Module)

This file implements a TCP client that connects to the server,
sends structured JSON requests, and displays responses received
from the server.

Networking concepts demonstrated:
- Client connections
- TCP sockets
- Request–response communication
- Protocol usage
"""

import socket
import json
import uuid

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5050


def build_request(request_type, payload):
    """
    Builds a JSON request following the agreed protocol.
    A unique request_id allows matching responses to requests.
    """
    return {
        "type": request_type,
        "request_id": str(uuid.uuid4()),
        "payload": payload
    }


def send_request(socket_obj, request):
    """
    Sends a request to the server and waits for a response.
    The response is returned as a Python dictionary.
    """
    socket_obj.sendall((json.dumps(request) + "\n").encode())

    response_line = socket_obj.makefile("r", encoding="utf-8").readline()
    return json.loads(response_line.strip())


def display_response(response):
    """
    Displays server responses in a readable format.
    """
    print("\n--- Server Response ---")
    print(f"Status: {response['status']}")

    if response["status"] == "OK":
        print(json.dumps(response["data"], indent=2))
    else:
        print("Error:", response["error"])

    print("------------------------\n")


def main():
    """
    Main client loop.
    Presents a menu to the user and sends requests
    based on user input.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Connected to server.\n")

        while True:
            print("1) ECHO")
            print("2) SYSTEM_INFO")
            print("3) FILE_QUERY")
            print("4) HELP")
            print("5) EXIT")

            choice = input("Select an option: ").strip()

            if choice == "1":
                msg = input("Enter message: ")
                req = build_request("ECHO", {"message": msg})

            elif choice == "2":
                req = build_request("SYSTEM_INFO", {})

            elif choice == "3":
                key = input("Enter key: ")
                req = build_request("FILE_QUERY", {"key": key})

            elif choice == "4":
                req = build_request("HELP", {})

            elif choice == "5":
                print("Exiting client.")
                break

            else:
                print("Invalid choice.\n")
                continue

            response = send_request(client_socket, req)
            display_response(response)


if __name__ == "__main__":
    main()
