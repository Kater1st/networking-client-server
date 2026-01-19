
Networking Module - README
Tinashe Allan Katenaire

Overview
This project demonstrates the design and implementation of a networked client–server application using Python. The goal of the project was to deepen my understanding of how computers communicate over a network using the TCP/IP stack, structured message formats, and a clearly defined communication protocol.

The software consists of two separate programs: a server and a client. The server listens for incoming connections on a specific port and processes requests from connected clients. The client connects to the server, sends structured requests, and displays the responses returned by the server. Communication between the client and server is performed using JSON-formatted messages transmitted over a TCP connection.

To use the software, the server must be started first so that it begins listening for client connections. Once the server is running, the client can be started in a separate terminal. The client presents a menu that allows the user to send different types of requests to the server and view the responses.

The purpose of writing this software was to practice building reliable networked applications, design a simple but effective communication protocol, and gain hands-on experience with sockets, ports, and request–response communication patterns that are commonly used in real-world software systems.

Software Demo Video:
https://youtu.be/XdChlbPpYdI

Network Communication
The software uses a client–server architecture. In this model, the server waits for incoming connections and can handle requests from multiple clients, while the client initiates communication by sending requests and waiting for responses.

The application uses TCP (Transmission Control Protocol) to ensure reliable and ordered delivery of data between the client and server. The server listens on port 5050, and the client connects to this port to establish communication.

Messages exchanged between the client and server are formatted using JSON. Each request sent by the client includes a request type, a unique request identifier, and a payload containing any necessary data. The server responds with a JSON object that includes the same request identifier, a status indicating success or failure, and either response data or an error description. Messages are sent using newline-delimited JSON to clearly separate individual requests and responses.

OSI Model Alignment
This project demonstrates multiple layers of the OSI model in a practical implementation. At the application layer, the client and server communicate using a structured JSON-based protocol that defines request and response formats. At the transport layer, TCP is used to provide reliable, ordered, and error-checked delivery of messages. The network layer enables communication between devices using IP addressing and port numbers. Together, these layers allow structured data to be transmitted from the client, processed by the server, and returned in a predictable and consistent format.

Communication Protocol Specification
All messages in this system follow a defined request–response protocol using JSON. Each message is transmitted as a single JSON object followed by a newline character to indicate message boundaries.

Request Format:
{
  "type": "REQUEST_TYPE",
  "request_id": "unique-id",
  "payload": {}
}

Response Format:
{
  "request_id": "unique-id",
  "status": "OK | ERROR",
  "data": {},
  "error": null
}

The protocol supports the following request types:
- ECHO – Sends a message to the server and receives the same message in the response
- SYSTEM_INFO – Requests server metadata such as server name, time, and active client count
- FILE_QUERY – Requests data from a local JSON file hosted on the server
- HELP – Returns a list of supported request types

Development Environment
The software was developed using Visual Studio Code as the primary code editor and Git/GitHub for version control and source code management. The programs were tested locally by running the client and server in separate terminal windows.

The application was written in Python, using only standard libraries. The socket library was used to implement TCP networking, the json library was used to format and parse structured messages, and the threading library was used on the server to allow multiple clients to connect simultaneously.

Testing and Validation
The system was tested using multiple test cases to verify correct behavior and reliability. These tests included sending valid requests for each supported request type and verifying that the server returned structured and accurate responses. Error-handling tests were also performed by sending invalid or unsupported requests, as well as requesting missing keys in the local data file, to ensure the server returned appropriate error messages without crashing.

Security Considerations
This implementation focuses on core networking concepts and does not include authentication or encrypted communication. In a production environment, this system could be extended to use secure transport mechanisms such as TLS to protect data in transit and authentication mechanisms to restrict access to authorized clients. Input validation on the server helps reduce the risk of malformed or malicious requests.

Useful Websites
Python Socket Programming Documentation: https://docs.python.org/3/library/socket.html
TCP/IP and Client–Server Model – Wikipedia: https://en.wikipedia.org/wiki/Client%E2%80%93server_model
OSI Model Overview – Wikipedia: https://en.wikipedia.org/wiki/OSI_model
JSON Format Documentation: https://www.json.org/json-en.html

Future Work
- Implement TLS encryption to secure communication between the client and server
- Add user authentication and access control for client connections
- Develop a graphical user interface (GUI) for improved usability
- Extend the protocol to support file transfer and data modification requests
- Deploy the server to a cloud environment for remote client access


Author

Tinashe Allan Katenaire
