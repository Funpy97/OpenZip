import ipaddress
import socket
import threading
from typing import Iterator, List

import more_itertools

from openzip.networking.messages import Messages
from openzip.networking.netinfo import NetworkInfo
from openzip.utils.constants import DEFAULT_CONNECTION_BUFFER, SCANNER_THREADS, DEFAULT_SERVER_PORT


class ScannedServer:
    def __init__(self, _id: str, ip: str, port: int):
        """
        Store information about a ZipServer
        """
        self.id = _id
        self.ip = ip
        self.port = port

    def __str__(self) -> str:
        return f"<ScannedServer id={self.id}, ip={self.ip}, port={self.port}>"


class BaseScanner:
    def __init__(self):
        self._servers = []

    def get_servers(self) -> List[ScannedServer]:
        """
        Search ZipServer(s) in the local network, based on the subnet mask.

        :return: a list of ScannedServer instances
        """
        self._servers = []
        threads = []

        local_network = ipaddress.IPv4Network(f"{NetworkInfo().local_ipv4}/{NetworkInfo().subnet_mask}", strict=False)

        for hosts in more_itertools.distribute(SCANNER_THREADS, local_network.hosts()):
            thread = threading.Thread(target=self.__scan__, args=(hosts,))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        return self._servers

    def __scan__(self, addresses: Iterator[ipaddress.IPv4Address]):
        for address in addresses:
            try:
                sock = socket.socket()
                sock.settimeout(0.5)
                sock.connect((address.exploded, DEFAULT_SERVER_PORT))
                sock.send(Messages.scan)
                server_id = sock.recv(DEFAULT_CONNECTION_BUFFER)
                sock.close()

                self._servers.append(ScannedServer(_id=server_id.decode(),
                                                   ip=address.exploded,
                                                   port=DEFAULT_SERVER_PORT))

            except TimeoutError:
                continue


if __name__ == "__main__":
    scanner = BaseScanner()
    servers = scanner.get_servers()

    for server in servers:
        print(server)
