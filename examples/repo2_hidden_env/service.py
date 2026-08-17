import os

PORT = int(os.environ["SERVICE_PORT"])


def start() -> str:
    return f"listening on {PORT}"
