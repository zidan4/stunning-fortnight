import socket
import threading
import time

def handle_client(client_socket, client_address):
    try:
        print(f"Connection from {client_address}")

        # Simulate a delay to make it seem like a real service
        time.sleep(1)

        # Receive data (even if we don't do anything with it)
        data = client_socket.recv(1024)
        if data:
            print(f"Received data: {data.decode()}")

        # Log the interaction
        with open("honeypot.log", "a") as log_file:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Connection from {client_address} - Data: {data.decode() if data else 'None'}\n")

        # Send a generic response (optional)
        client_socket.send(b"OK\n")

    except Exception as e:
        print(f"Error handling client: {e}")
        with open("honeypot.log", "a") as log_file:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Error with {client_address} - {e}\n")

    finally:
        client_socket.close()
        print(f"Connection with {client_address} closed.")


def main():
    host = "0.0.0.0"  # Listen on all interfaces
    port = 12345      # Choose a non-standard port (or one you want to monitor)

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)  # Allow up to 5 queued connections

        print(f"Honeypot listening on {host}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()

    except Exception as e:
        print(f"Error starting honeypot: {e}")
    finally:
      if 'server_socket' in locals():
        server_socket.close()

if __name__ == "__main__":
    main()

    
