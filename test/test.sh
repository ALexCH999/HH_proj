


dd if=/dev/urandom of=testfile bs=1M count=2


python src/tcp_server.py testfile &
TCP_SERVER_PID=$!


python src/tcp_client.py tcp_downloaded_file


md5sum testfile tcp_downloaded_file


kill $TCP_SERVER_PID


python src/udp_server.py testfile &
UDP_SERVER_PID=$!


python src/udp_client.py udp_downloaded_file


md5sum testfile udp_downloaded_file


kill $UDP_SERVER_PID


rm testfile tcp_downloaded_file udp_downloaded_file