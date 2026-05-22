# ╔══════════════════════════════════════════════════╗
# ║      🐝 COG: ВАЙТЛИСТ «УЛЕЙ»                     ║
# ╚══════════════════════════════════════════════════╝

import discord
from discord.ext import commands

import config
import embeds as em
from whitelist_views import WhitelistApplyView
from logger import log


class WhitelistCog(commands.Cog, name="Вайтлист"):
    """Cog для работы с системой белого списка."""

    def __init__(self, bot: discord.Bot):
        self.bot = bot

    # ──────────────────────────────────────────────
    #  📌 SLASH-КОМАНДА /белый_список
    # ──────────────────────────────────────────────

    @discord.slash_command(
        name="белый_список",
        description="🐝 Подать заявку на вступление в белый список сервера «Улей»",
        guild_ids=[config.GUILD_ID]
    )
    async def whitelist_command(self, ctx: discord.ApplicationContext):
        """
        Отправляет embed с кнопкой подачи заявки на вайтлист.
        Доступна всем участникам сервера.
        """
        embed = em.embed_whitelist_welcome()
        view  = WhitelistApplyView()

        await ctx.respond(embed=embed, view=view)
        log.info(f"📋 {ctx.author} вызвал /белый_список")


def setup(bot: discord.Bot):
    bot.add_cog(WhitelistCog(bot))
    log.info("✅ Cog 'Вайтлист' загружен")
