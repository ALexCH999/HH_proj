import socket
import os
import struct
import zlib
from typing import NoReturn

CHUNK_SIZE = 4096 - 8  # 8 байт для номера пакета и контрольной суммы


def send_udp_file(file_path: str) -> NoReturn:
    """
    Отправляет файл через UDP с проверкой целостности и нумерацией пакетов.

    Args:
        file_path: Путь к файлу для отправки.
    """
    host = '127.0.0.1'
    port = 8081

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((host, port))
        print(f"UDP-сервер запущен на {host}:{port}")

        while True:
            _, client_addr = sock.recvfrom(8)  # Ожидаем запрос
            print(f"Получен запрос от {client_addr}")

            try:
                file_size = os.path.getsize(file_path)
                sock.sendto(struct.pack('!Q', file_size), client_addr)  # Отправляем размер файла

                with open(file_path, 'rb') as file:
                    packet_number = 0
                    while True:
                        chunk = file.read(CHUNK_SIZE)
                        if not chunk:
                            break

                        crc32 = zlib.crc32(chunk)
                        packet = struct.pack('!II', packet_number, crc32) + chunk
                        sock.sendto(packet, client_addr)

                        # Ожидаем подтверждение
                        try:
                            ack, _ = sock.recvfrom(4)
                            if ack == struct.pack('!I', packet_number):
                                packet_number += 1
                        except socket.timeout:
                            continue  # Повторная отправка

                    # Отправляем завершающий пакет
                    sock.sendto(struct.pack('!II', 0xFFFFFFFF, 0), client_addr)
            except Exception as e:
                print(f"Ошибка при отправке файла: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Использование: python udp_server.py <путь_к_файлу>")
        sys.exit(1)
    send_udp_file(sys.argv[1])