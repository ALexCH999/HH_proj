import socket
from typing import NoReturn


def request_file_tcp(file_name: str, server_ip: str = '127.0.0.1', server_port: int = 8080) -> NoReturn:
    """
    Запрашивает файл у TCP-сервера и сохраняет его локально.

    Args:
        file_name: Имя файла для сохранения.
        server_ip: IP-адрес сервера.
        server_port: Порт сервера.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_ip, server_port))
        print(f"Запрашиваем файл с {server_ip}:{server_port}")

        file_size = int(client_socket.recv(1024).decode())  # Получаем размер файла
        received_size = 0

        with open(file_name, 'wb') as file:
            while received_size < file_size:
                data = client_socket.recv(4096)
                file.write(data)
                received_size += len(data)
        print(f"Файл успешно загружен: {file_name}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Использование: python tcp_client.py <имя_файла>")
        sys.exit(1)
    request_file_tcp(sys.argv[1])