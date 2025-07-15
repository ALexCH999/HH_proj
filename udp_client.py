import socket
import struct
import zlib
from typing import NoReturn

CHUNK_SIZE = 4096 - 8


def request_udp_file(file_name: str, server_ip: str = '127.0.0.1', server_port: int = 8081) -> NoReturn:
    """
    Запрашивает файл через UDP и сохраняет его локально.

    Args:
        file_name: Имя файла для сохранения.
        server_ip: IP-адрес сервера.
        server_port: Порт сервера.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(5)
        sock.sendto(b'REQUEST', (server_ip, server_port))

        file_size_data, _ = sock.recvfrom(8)
        file_size = struct.unpack('!Q', file_size_data)[0]
        received_size = 0

        with open(file_name, 'wb') as file:
            expected_packet = 0
            while received_size < file_size:
                try:
                    packet, addr = sock.recvfrom(CHUNK_SIZE + 8)
                    packet_number, crc32 = struct.unpack('!II', packet[:8])
                    data = packet[8:]

                    if packet_number == 0xFFFFFFFF:  # Завершающий пакет
                        break

                    if packet_number == expected_packet and zlib.crc32(data) == crc32:
                        file.write(data)
                        received_size += len(data)
                        expected_packet += 1
                        sock.sendto(struct.pack('!I', packet_number), addr)  # Подтверждение
                except socket.timeout:
                    continue  # Повторный запрос

        print(f"Файл успешно загружен: {file_name}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Использование: python udp_client.py <имя_файла>")
        sys.exit(1)
    request_udp_file(sys.argv[1])