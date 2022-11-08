import re
import socket
import subprocess
import sys

import requests


class NetworkInfo:
    """
    Get information about the local IP, public IP and subnet mask.
    """
    @property
    def subnet_mask(self) -> str:
        platform = sys.platform
        default_mask = "255.255.255.0"

        try:
            if platform.startswith("win"):
                cmd = subprocess.check_output("ipconfig")
                result = re.findall("mask.*", cmd.decode(), re.IGNORECASE)[0]
                mask = re.findall(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", result)[0]

            elif platform.startswith("linux"):
                # TODO: implement for linux
                mask = default_mask

            elif platform.startswith("darwin"):
                # TODO: implement for Mac OS X
                mask = default_mask

            else:
                mask = default_mask

        except IndexError:
            mask = default_mask

        return mask

    @property
    def local_ipv4(self) -> str:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)

        try:
            s.connect(("8.8.8.8", 1))
            ip = s.getsockname()[0]

        except socket.error:
            ip = "127.0.0.1"

        finally:
            s.close()

        return ip

    @property
    def public_ipv4(self) -> str:
        urls = ["https://api.ipify.org", "https://ip.seeip.org"]

        for url in urls:
            try:
                return requests.get(url).text

            except requests.RequestException:
                continue

        return str()

    def __str__(self):
        return f"IPv4 Info\nLocal: {self.local_ipv4}\nPublic: {self.public_ipv4}"


if __name__ == "__main__":
    network = NetworkInfo()
    print(network.subnet_mask)
