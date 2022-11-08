import random
import string


def digits_id(length=9) -> str:
    return "".join([random.choice(string.digits) for _ in range(length)])


def new_client_id() -> str:
    return "C" + digits_id()


def new_server_id() -> str:
    return "S" + digits_id()


if __name__ == "__main__":
    ncid = new_client_id()
    nsid = new_server_id()

    print(f"CLIENT ID: {ncid}\nSERVER ID: {nsid}")
