import subprocess
import os
import sys
import time
import socket

# Optional: reduce transformers logs
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"

# Start Django server silently
with open(os.devnull, "w") as null:
    subprocess.Popen(
        [sys.executable, "manage.py", "runserver"],
        stdout=null,
        stderr=null
    )

# Wait until port 8000 is open
def wait_for_server(host="127.0.0.1", port=8000, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except (ConnectionRefusedError, socket.timeout):
            time.sleep(0.5)
    return False

if wait_for_server():
    print("Server running at: http://127.0.0.1:8000/")
else:
    print("Error: Server failed to start.")
