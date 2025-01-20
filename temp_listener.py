import socket

def start_server(host, port):
    try:
        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the host and port
        server_socket.bind((host, port))

        # Listen for incoming connections
        server_socket.listen(5)
        print(f"[+] Listening on {host}:{port}")

        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print(f"[+] Connection established with {client_address}")

        while True:
            # Get command from the user
            command = input("Shell> ").strip()

            if not command:
                continue

            # Send command to the client
            client_socket.send(command.encode('utf-8'))

            if command.lower() == "exit":
                print("[+] Closing connection")
                break

            # Receive the response from the client
            response = client_socket.recv(4096).decode('utf-8')
            print(response, end="")

        client_socket.close()
        server_socket.close()

    except Exception as e:
        print(f"[-] Error: {str(e)}")

if __name__ == "__main__":
    SERVER_HOST = "0.0.0.0"  # Listen on all interfaces
    SERVER_PORT = 787

    start_server(SERVER_HOST, SERVER_PORT)