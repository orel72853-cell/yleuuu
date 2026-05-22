# ╔══════════════════════════════════════════════════╗
# ║        🐝 ГЛАВНЫЙ ФАЙЛ БОТА «УЛЕЙ»               ║
# ║   Точка входа — запуск и загрузка всех cogs      ║
# ╚══════════════════════════════════════════════════╝

import discord
import sys
import os

import config
from logger import log, print_startup_banner


# ──────────────────────────────────────────────────────
#  🔧 СПИСОК COGS ДЛЯ АВТОЗАГРУЗКИ
# ──────────────────────────────────────────────────────

COGS = [
    "events",       # ⚡ Системные события (on_ready, ошибки)
    "whitelist",    # 🐝 Команда /белый_список
    "rules",        # 📜 Команда /правила
    "news",         # 📰 Команда /новости
]


# ──────────────────────────────────────────────────────
#  🤖 ИНИЦИАЛИЗАЦИЯ БОТА
# ──────────────────────────────────────────────────────

intents = discord.Intents.default()
intents.members        = True   # Нужно для выдачи ролей и отслеживания участников
intents.message_content = True  # Нужно для чтения сообщений

bot = discord.Bot(
    intents=intents,
    description=f"🐝 Бот сервера «{config.SERVER_NAME}»"
)


# ──────────────────────────────────────────────────────
#  📦 ЗАГРУЗКА COGS
# ──────────────────────────────────────────────────────

def load_cogs():
    """Загружает все cogs из списка COGS."""
    loaded  = 0
    failed  = 0

    log.info("─" * 50)
    log.info("📦 Загрузка модулей (cogs)...")

    for cog in COGS:
        try:
            bot.load_extension(cog)
            loaded += 1
            log.info(f"  ✅ {cog}.py — загружен")
        except Exception as e:
            failed += 1
            log.error(f"  ❌ {cog}.py — ОШИБКА: {e}", exc_info=True)

    log.info("─" * 50)
    log.info(f"📊 Загружено: {loaded} | Ошибок: {failed}")

    if failed > 0:
        log.warning("⚠️ Некоторые модули не загружены. Проверь логи выше.")


# ──────────────────────────────────────────────────────
#  🚀 ТОЧКА ЗАПУСКА
# ──────────────────────────────────────────────────────

if __name__ == "__main__":
    # Красивый баннер при старте
    print_startup_banner()

    # Проверяем токен
    if not config.TOKEN:
        log.critical(
            "❌ Токен не указан! Открой config.py и вставь TOKEN = 'твой_токен'"
        )
        sys.exit(1)

    # Загружаем все cogs
    load_cogs()

    # Запускаем бота
    log.info("🚀 Запуск бота...")
    try:
        bot.run(config.TOKEN)
    except discord.LoginFailure:
        log.critical("❌ Неверный токен бота! Проверь config.py")
        sys.exit(1)
    except KeyboardInterrupt:
        log.info("🛑 Бот остановлен вручную")
    except Exception as e:
        log.critical(f"💥 Критическая ошибка запуска: {e}", exc_info=True)
        sys.exit(1)
