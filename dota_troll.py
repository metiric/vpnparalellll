"""
Шуточная программа для двоюродного брата.
Раз в случайный промежуток 5-30 минут закрывает Dota 2
и показывает смешное окно с "ошибкой".

Запуск:  python dota_troll.py
Остановка: Ctrl+C в консоли (или закрыть окно консоли)

Работает на Windows. Требует Python 3.
"""

import os
import sys
import time
import random
import subprocess
import platform
import tkinter as tk
from tkinter import messagebox

PROCESS_NAMES = ["dota2.exe", "Dota2.exe", "dota2"]

FUNNY_ERRORS = [
    ("CRITICAL ERROR 0xDEADBEEF",
     "Ошибка ядра: обнаружено превышение нормы Доты в крови.\n"
     "Рекомендуется: выйти на улицу, посмотреть на солнце, поздороваться с мамой."),
    ("STEAM ERROR 0x0BAD_F00D",
     "Steam обнаружил подозрительную активность:\n"
     "Игрок не моргал 47 минут. Сессия завершена для вашей же безопасности."),
    ("VALVE ANTI-NOLIFE SYSTEM",
     "Система Valve Anti-NoLife активирована.\n"
     "MMR заморожен до выполнения квеста: \"Сходить за хлебом\"."),
    ("NVIDIA DRIVER PANIC",
     "Видеокарта перегрелась от количества кеков на миду.\n"
     "Охлаждение: откройте окно и подышите воздухом 10 минут."),
    ("ERROR: REALITY.EXE NOT RESPONDING",
     "Не удалось найти процесс реальная_жизнь.exe\n"
     "Попробуйте перезапустить мозг (Ctrl+Alt+Улица)."),
    ("DOTA 2 CRASH REPORT #322",
     "Pudge снова не попал хуком. Сервер не выдержал испанского стыда\n"
     "и ушёл в отпуск."),
    ("WINDOWS DEFENDER",
     "Обнаружена угроза: \"Запойная катка\".\n"
     "Угроза нейтрализована. Хорошего дня!"),
    ("MMR PROTECTION SERVICE",
     "Ваш MMR был спасён от вас же.\n"
     "Следующая катка будет доступна после прогулки."),
    ("BSOD :)",
     "PAGE_FAULT_IN_NONPAGED_LIFE\n\n"
     "Ваш брат соскучился. Перезагрузка социальных связей..."),
    ("ERROR 404: GIRLFRIEND NOT FOUND",
     "Слишком много часов в Доте. Поиск девушки невозможен.\n"
     "Попробуйте выйти на улицу хотя бы раз."),
]


def kill_dota():
    system = platform.system()
    killed = False
    if system == "Windows":
        for name in PROCESS_NAMES:
            try:
                result = subprocess.run(
                    ["taskkill", "/F", "/IM", name],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    killed = True
            except Exception as e:
                print(f"[!] {e}")
    else:
        for name in PROCESS_NAMES:
            try:
                subprocess.run(["pkill", "-f", name], capture_output=True)
                killed = True
            except Exception as e:
                print(f"[!] {e}")
    return killed


def show_error_popup(title, message):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    try:
        root.iconbitmap(default="")
    except Exception:
        pass
    messagebox.showerror(title, message, parent=root)
    root.destroy()


def main():
    print("=" * 50)
    print(" Шуточный тролль для Доты запущен ")
    print(" Закрыть: Ctrl+C ")
    print("=" * 50)

    while True:
        wait_minutes = random.uniform(5, 30)
        wait_seconds = wait_minutes * 60
        next_time = time.strftime(
            "%H:%M:%S",
            time.localtime(time.time() + wait_seconds)
        )
        print(f"[i] Следующий троллинг через "
              f"{wait_minutes:.1f} мин (в {next_time})")

        try:
            time.sleep(wait_seconds)
        except KeyboardInterrupt:
            print("\n[i] Выход.")
            sys.exit(0)

        title, message = random.choice(FUNNY_ERRORS)
        print(f"[!] Бабах! Закрываем Dota 2... ({title})")

        was_killed = kill_dota()
        if was_killed:
            print("    Dota 2 успешно прибита.")
        else:
            print("    Dota 2 не запущена — просто покажем окно.")

        try:
            show_error_popup(title, message)
        except Exception as e:
            print(f"[!] Не удалось показать окно: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[i] Пока!")
