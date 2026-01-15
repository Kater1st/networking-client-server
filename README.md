Project Title

Multi-Service Client–Server Networking Application

Overview

This project demonstrates a client–server networking application built using Python and TCP sockets. The goal of the project is to show an understanding of how two computers (or two programs) communicate over a network using a defined protocol, structured messages, and a request–response model.

The application consists of two separate programs:

server.py – Listens for client connections and processes requests

client.py – Connects to the server, sends requests, and displays responses

The client and server communicate using JSON-formatted messages sent over a TCP connection.

Networking Concepts Demonstrated

This project demonstrates the following networking concepts:

Client–Server architecture

TCP communication

Sockets and ports

Request–response protocol design

Structured message formats (JSON)

Reading data from a local file over a network

Error handling and validation

These concepts align with the OSI model, where application data is structured at the application layer and transmitted reliably using the transport layer (TCP).

Communication Protocol

All communication between the client and server uses newline-delimited JSON. Each message is sent as a single JSON object followed by a newline character (\n).

Request Format (Client → Server)
{
  "type": "REQUEST_TYPE",
  "request_id": "unique-id",
  "payload": {}
}

Response Format (Server → Client)
{
  "request_id": "unique-id",
  "status": "OK | ERROR",
  "data": {},
  "error": null
}

Supported Request Types
1. ECHO

The client sends a message and the server responds by echoing the same message back.

2. SYSTEM_INFO

The server returns system-related information such as:

Server name

Current server time

Number of active client connections

3. FILE_QUERY

The server reads data from a local JSON file (data.json) and returns the requested value based on a provided key.

This request type demonstrates obtaining information from a local file in response to a network request.

4. HELP

Returns a list of all supported request types and how they can be used.

Local Data File

The server uses a local file named data.json to support the FILE_QUERY request type. This file contains key–value pairs that can be requested by the client.

How to Run the Project
Requirements

Python 3.x

No external libraries required

Steps

Start the server:

python server.py


In a separate terminal, start the client:

python client.py


Use the interactive menu in the client to send different request types to the server.

Error Handling

The server validates all incoming requests and returns structured error responses when:

JSON is invalid

A request type is unknown

Required fields are missing

A requested key is not found

This ensures reliable and predictable communication between the client and server.

Demo Video

A demonstration video showing the application running, a walkthrough of the code, and an explanation of the networking concepts is available at the following link:

[Insert your YouTube video link here]

Author

Tinashe Allan Katenaire
CSE 310 – Applied Programming