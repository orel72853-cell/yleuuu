# ╔══════════════════════════════════════════════════╗
# ║       📜 COG: ПРАВИЛА «УЛЕЙ»                     ║
# ╚══════════════════════════════════════════════════╝

import discord
from discord.ext import commands

import config
import embeds as em
from rules_views import RulesView
from logger import log


class RulesCog(commands.Cog, name="Правила"):
    """Cog для вывода правил сервера и теста."""

    def __init__(self, bot: discord.Bot):
        self.bot = bot

    # ──────────────────────────────────────────────
    #  📌 SLASH-КОМАНДА /правила
    # ──────────────────────────────────────────────

    @discord.slash_command(
        name="правила",
        description="📜 Просмотреть правила сервера «Улей»",
        guild_ids=[config.GUILD_ID]
    )
    async def rules_command(self, ctx: discord.ApplicationContext):
        """
        Выводит все правила сервера в красивых embed'ах
        и добавляет кнопку сдачи теста.
        """
        await ctx.defer()

        rule_embeds = em.embed_rules_all_list()
        view        = RulesView()

        # Отправляем первый embed с ответом
        await ctx.followup.send(embed=rule_embeds[0])

        # Остальные embed'ы — отдельными сообщениями
        for rule_embed in rule_embeds[1:]:
            await ctx.channel.send(embed=rule_embed)

        # Последнее сообщение с кнопкой теста
        final_embed = discord.Embed(
            title="📘 Готов сдать правила?",
            description=(
                "───────────────────────────────\n"
                "🧠 Нажми кнопку ниже, чтобы пройти **тест** по правилам.\n\n"
                "✅ Нужно правильно ответить на **4 из 5** вопросов.\n\n"
                "🐝 После прохождения теста ты сможешь **подать заявку** на вайтлист!\n"
                "───────────────────────────────"
            ),
            color=config.COLOR_GOLD
        )
        final_embed.set_footer(text=f"🐝 {config.SERVER_NAME}")

        await ctx.channel.send(embed=final_embed, view=view)
        log.info(f"📜 {ctx.author} вызвал /правила")


def setup(bot: discord.Bot):
    bot.add_cog(RulesCog(bot))
    log.info("✅ Cog 'Правила' загружен")
