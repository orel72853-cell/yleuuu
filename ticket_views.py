# ╔══════════════════════════════════════════════════╗
# ║        🎫 TICKET VIEWS БОТА «УЛЕЙ»               ║
# ╚══════════════════════════════════════════════════╝

# Этот модуль экспортирует все view'ы для тикетов.
# Основная логика находится в whitelist_views.py.
# Здесь находятся вспомогательные компоненты.

import discord
import config
from logger import log


class TicketCloseView(discord.ui.View):
    """
    View с кнопкой закрытия тикета.
    Добавляется модератором при необходимости ручного закрытия.
    """

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="🗑️ Закрыть тикет",
        style=discord.ButtonStyle.danger,
        custom_id="ticket_close_btn"
    )
    async def close_button(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        mod_role = interaction.guild.get_role(config.MODERATOR_ROLE_ID)
        is_mod   = mod_role in interaction.user.roles if mod_role else False

        if not is_mod:
            await interaction.response.send_message(
                "🛡️ Только модераторы могут закрывать тикеты!", ephemeral=True
            )
            return

        await interaction.response.send_message(
            "🗑️ Тикет будет закрыт через **5 секунд**...",
        )
        log.info(f"🗑️ Тикет {interaction.channel.name} закрыт модератором {interaction.user}")

        import asyncio
        await asyncio.sleep(5)

        try:
            await interaction.channel.delete(reason=f"Тикет закрыт модератором {interaction.user}")
        except Exception as e:
            log.error(f"💥 Ошибка закрытия тикета: {e}")
