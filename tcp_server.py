import socket
import os
from typing import NoReturn


def start_tcp_server(file_path: str) -> NoReturn:
    """
    Запускает TCP-сервер для передачи файла по запросу клиента.

    Args:
        file_path: Путь к файлу, который будет отправляться клиентам.
    """
    host = '127.0.0.1'
    port = 8080

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"TCP-сервер запущен на {host}:{port}")

        while True:
            conn, addr = server_socket.accept()
            print(f"Получен запрос от {addr}")

            try:
                with open(file_path, 'rb') as file:
                    file_size = os.path.getsize(file_path)
                    conn.sendall(str(file_size).encode())  # Отправляем размер файла
                    data = file.read(4096)
                    while data:
                        conn.sendall(data)
                        data = file.read(4096)
                print(f"Файл успешно отправлен клиенту {addr}")
            except Exception as e:
                print(f"Ошибка при отправке файла: {e}")
            finally:
                conn.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Использование: python tcp_server.py <путь_к_файлу>")
        sys.exit(1)
    start_tcp_server(sys.argv[1])