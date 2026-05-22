# ╔══════════════════════════════════════════════════╗
# ║       📰 COG: НОВОСТИ «УЛЕЙ»                     ║
# ╚══════════════════════════════════════════════════╝

import discord
from discord.ext import commands

import config
import embeds as em
from checks import is_moderator
from logger import log


class NewsCog(commands.Cog, name="Новости"):
    """Cog для публикации новостей сервера."""

    def __init__(self, bot: discord.Bot):
        self.bot = bot

    # ──────────────────────────────────────────────
    #  📌 SLASH-КОМАНДА /новости
    # ──────────────────────────────────────────────

    @discord.slash_command(
        name="новости",
        description="📰 Опубликовать новость сервера «Улей» (только для модераторов)",
        guild_ids=[config.GUILD_ID]
    )
    @is_moderator()
    async def news_command(
        self,
        ctx: discord.ApplicationContext,
        заголовок: discord.Option(
            str,
            description="📰 Заголовок новости",
            required=True,
            max_length=200
        ),
        текст: discord.Option(
            str,
            description="📝 Текст новости",
            required=True,
            max_length=2000
        ),
        изображение: discord.Option(
            str,
            description="🖼️ Ссылка на изображение (необязательно)",
            required=False,
            default=None
        )
    ):
        """
        Публикует красивую новость с ping @everyone.
        Только для модераторов.
        """
        await ctx.defer()

        embed = em.embed_news(
            title=заголовок,
            text=текст,
            author=ctx.author,
            image_url=изображение
        )

        # Отправляем новость с разрешённым @everyone
        await ctx.followup.send(
            content="@everyone",
            embed=embed,
            allowed_mentions=discord.AllowedMentions(everyone=True)
        )

        log.info(
            f"📰 Новость опубликована | автор: {ctx.author} | заголовок: «{заголовок}»"
        )


def setup(bot: discord.Bot):
    bot.add_cog(NewsCog(bot))
    log.info("✅ Cog 'Новости' загружен")
