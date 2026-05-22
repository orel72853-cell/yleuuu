# ╔══════════════════════════════════════════════════╗
# ║      ⚡ COG: СОБЫТИЯ БОТА «УЛЕЙ»                  ║
# ╚══════════════════════════════════════════════════╝

import discord
from discord.ext import commands

import config
from logger import log


class EventsCog(commands.Cog, name="События"):
    """Cog для обработки системных событий Discord."""

    def __init__(self, bot: discord.Bot):
        self.bot = bot

    # ──────────────────────────────────────────────
    #  ✅ СОБЫТИЕ: Бот готов
    # ──────────────────────────────────────────────

    @commands.Cog.listener()
    async def on_ready(self):
        """Вызывается когда бот полностью загружен."""
        log.info("=" * 55)
        log.info(f"🐝 Бот запущен как : {self.bot.user}")
        log.info(f"🆔 ID бота         : {self.bot.user.id}")
        log.info(f"🏰 Серверов        : {len(self.bot.guilds)}")
        log.info(f"👥 Участников      : {sum(g.member_count for g in self.bot.guilds)}")
        log.info("=" * 55)

        # Устанавливаем статус бота
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="🐝 Следит за ульем"
            )
        )
        log.info("🎭 Статус установлен: «🐝 Следит за ульем»")

    # ──────────────────────────────────────────────
    #  ⚠️ СОБЫТИЕ: Ошибка команды
    # ──────────────────────────────────────────────

    @commands.Cog.listener()
    async def on_application_command_error(
        self,
        ctx: discord.ApplicationContext,
        error: discord.DiscordException
    ):
        """Глобальный обработчик ошибок slash-команд."""

        if isinstance(error, commands.CheckFailure):
            # Ошибки проверки прав — уже обработаны в checks.py
            return

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(
                f"⏳ Команда на кулдауне. Подожди **{error.retry_after:.1f}** сек.",
                ephemeral=True
            )
            return

        if isinstance(error, discord.Forbidden):
            await ctx.respond(
                "❌ У бота не хватает прав для выполнения этого действия.",
                ephemeral=True
            )
            log.error(f"🔒 Forbidden error в команде {ctx.command}: {error}")
            return

        # Неизвестные ошибки
        log.error(f"💥 Ошибка в команде /{ctx.command}: {error}", exc_info=True)
        try:
            await ctx.respond(
                "💥 Произошла внутренняя ошибка. Сообщи администрации!",
                ephemeral=True
            )
        except Exception:
            pass

    # ──────────────────────────────────────────────
    #  👋 СОБЫТИЕ: Новый участник
    # ──────────────────────────────────────────────

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Логируем когда кто-то заходит на сервер."""
        if member.guild.id != config.GUILD_ID:
            return

        log.info(f"👋 Новый участник: {member} ({member.id})")

    # ──────────────────────────────────────────────
    #  🚪 СОБЫТИЕ: Участник вышел
    # ──────────────────────────────────────────────

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """Логируем когда кто-то покидает сервер."""
        if member.guild.id != config.GUILD_ID:
            return

        log.info(f"🚪 Участник покинул: {member} ({member.id})")

        # Если был открыт тикет — логируем
        import json
        try:
            with open("tickets.json", "r", encoding="utf-8") as f:
                tickets = json.load(f)
            if str(member.id) in tickets:
                log.warning(
                    f"⚠️ Участник с открытым тикетом покинул сервер: {member}"
                )
        except Exception:
            pass


def setup(bot: discord.Bot):
    bot.add_cog(EventsCog(bot))
    log.info("✅ Cog 'События' загружен")
