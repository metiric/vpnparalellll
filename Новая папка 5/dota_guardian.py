import os
import sys
import time
import random
import psutil
import ctypes
import threading
import socket
from datetime import datetime

# --- НАСТРОЙКИ ---
PASSWORD = "wake_up_sanya"
PORT = 65432

# 5 жутких ошибок (железо + имитация палева читов/VAC)
errors = [
    "Valve Anti-Cheat Error: Unauthorized memory patch detected at offset 0x7FF6B. Client integrity compromised. (Error Code: 1114)",
    "Direct3D 11 Error: Overlay hook failed to initialize. D3D11CreateDeviceAndSwapChain returned E_FAIL.",
    "Unhandled Exception: EXCEPTION_ACCESS_VIOLATION (0xc0000005) at VTable index 12. Attempted to execute arbitrary code.",
    "CSchemaSystem::Load(): VPK signature mismatch or corrupted memory allocation. Please verify integrity of game files.",
    "Engine Error: DXGI_ERROR_DEVICE_HUNG. The application's device failed due to badly formed commands."
]


def kill_dota(show_error=True):
    for proc in psutil.process_iter(['name']):
        try:
            name = (proc.info['name'] or "").lower()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

        if name == "dota2.exe":
            try:
                # 35% шанс на жёсткое аппаратное зависание перед вылетом
                if show_error and random.randint(1, 100) <= 35:
                    proc.suspend()      # картинка виснет намертво
                    time.sleep(12)      # держим в страхе 12 секунд
                    proc.resume()       # размораживаем, чтобы убить без сопротивления ОС

                proc.kill()

                if show_error:
                    msg = random.choice(errors)
                    threading.Thread(
                        target=lambda: ctypes.windll.user32.MessageBoxW(
                            0, msg, "Dota 2 - Fatal Error", 0x10 | 0x0
                        ),
                        daemon=True
                    ).start()
                return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    return False


def dota_guardian():
    next_crash_time = time.time() + random.randint(5 * 60, 30 * 60)

    while True:
        current_hour = datetime.now().hour

        # Комендантский час (23:00 - 05:59): тихое убийство без окон
        if current_hour >= 23 or current_hour < 6:
            kill_dota(show_error=False)
            time.sleep(3)
            continue

        # Дневной режим: рандомные краши
        if time.time() >= next_crash_time:
            if kill_dota(show_error=True):
                next_crash_time = time.time() + random.randint(5 * 60, 30 * 60)

        time.sleep(10)


def admin_listener():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(('localhost', PORT))
    except OSError as e:
        print(f"Не удалось занять порт {PORT}: {e}")
        sys.exit(1)
    server.listen(1)

    while True:
        conn, addr = server.accept()
        try:
            data = conn.recv(1024).decode('utf-8', errors='ignore').strip()
            if data == PASSWORD:
                conn.sendall(b"Access granted. Shutting down...\n")
                conn.close()
                os._exit(0)
            else:
                conn.sendall(b"Access denied.\n")
        finally:
            conn.close()


if __name__ == "__main__":
    guardian_thread = threading.Thread(target=dota_guardian, daemon=True)
    guardian_thread.start()
    admin_listener()
