# ╔══════════════════════════════════════════════════╗
# ║           📜 ЛОГГЕР БОТА «УЛЕЙ»                  ║
# ╚══════════════════════════════════════════════════╝

import logging
import sys
from datetime import datetime

# ─── Настройка форматтера ───────────────────────────
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def setup_logger(name: str = "Улей") -> logging.Logger:
    """
    Создаёт и возвращает настроенный логгер.
    Логи выводятся в консоль с цветами и временем.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Избегаем дублирования хендлеров
    if logger.handlers:
        return logger

    # ─── Консольный хендлер ───
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def print_startup_banner():
    """🐝 Красивый стартовый баннер при запуске бота."""
    banner = r"""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║    🐝  Б О Т   « У Л Е Й »   З А П У С К А Е Т С Я  🐝  ║
║                                                          ║
║         ⠀⠀⠀⣠⡴⠒⠋⠉⠉⠉⠙⠒⢦⣄⠀⠀⠀                            ║
║         ⠀⠀⣰⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠈⢳⡀⠀                            ║
║         ⠀⢠⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡄                            ║
║         ⠀⣿⣿⡄⠀⠀⠀🐝⠀⠀⠀⠀⢀⣿⣿                            ║
║         ⠀⢿⣿⣷⣦⣤⣤⣤⣤⣤⣤⣴⣾⣿⡿                            ║
║         ⠀⠈⠙⠻⢿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠁                            ║
║                                                          ║
║   📜 Minecraft RP  ⚔️ PvP  🛡️ Защита  🐝 Сообщество  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""
    print(banner)
    print(f"  🕐 Время запуска : {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    print(f"  📦 Версия        : 1.0.0")
    print(f"  👤 Разработка    : Администрация «Улей»")
    print("─" * 62)


# ─── Глобальный логгер ───────────────────────────────
log = setup_logger("Улей")
