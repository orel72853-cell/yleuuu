# ╔══════════════════════════════════════════════════╗
# ║      🐝 VIEWS & MODALS ВАЙТЛИСТА «УЛЕЙ»          ║
# ╚══════════════════════════════════════════════════╝

import discord
import json
import os
import asyncio

import config
import embeds as em
from checks import send_safe
from logger import log


# ──────────────────────────────────────────────────────
#  📝 MODAL — форма заявки
# ──────────────────────────────────────────────────────

class WhitelistModal(discord.ui.Modal):
    """Модальное окно с вопросами для вступления в вайтлист."""

    def __init__(self):
        super().__init__(title="🐝 Заявка на вайтлист «Улей»")

        self.nickname = discord.ui.InputText(
            label="🐝 Ник в Minecraft",
            placeholder="Твой никнейм в игре...",
            min_length=3,
            max_length=16
        )
        self.age = discord.ui.InputText(
            label="🎂 Сколько тебе лет?",
            placeholder="Например: 17",
            min_length=1,
            max_length=3
        )
        self.adequacy = discord.ui.InputText(
            label="🧠 Что для тебя значит адекватность?",
            placeholder="Опиши своими словами...",
            style=discord.InputTextStyle.long,
            min_length=10,
            max_length=500
        )
        self.reason = discord.ui.InputText(
            label="🌿 Зачем ты пришёл на сервер?",
            placeholder="Расскажи о своих целях...",
            style=discord.InputTextStyle.long,
            min_length=10,
            max_length=500
        )

        self.add_item(self.nickname)
        self.add_item(self.age)
        self.add_item(self.adequacy)
        self.add_item(self.reason)

    async def callback(self, interaction: discord.Interaction):
        """Обработка отправки формы — создание тикета."""
        await interaction.response.defer(ephemeral=True)

        guild   = interaction.guild
        member  = interaction.user
        nick    = self.nickname.value.strip()
        age     = self.age.value.strip()
        adequacy = self.adequacy.value.strip()
        reason  = self.reason.value.strip()

        # ── Проверка: нет ли уже открытого тикета ──────
        tickets = _load_tickets()
        if str(member.id) in tickets:
            await interaction.followup.send(
                "⚠️ У тебя уже есть открытая заявка! Дождись решения модераторов.",
                ephemeral=True
            )
            return

        # ── Получаем категорию ─────────────────────────
        category = guild.get_channel(config.WHITELIST_CATEGORY_ID)
        if category is None:
            await interaction.followup.send(
                "❌ Категория для тикетов не найдена. Обратись к администрации.",
                ephemeral=True
            )
            log.error(f"❌ Категория {config.WHITELIST_CATEGORY_ID} не найдена!")
            return

        # ── Права доступа к тикету ─────────────────────
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),
            guild.me: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_channels=True
            ),
        }

        # Добавляем роль модератора если есть
        mod_role = guild.get_role(config.MODERATOR_ROLE_ID)
        if mod_role:
            overwrites[mod_role] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            )

        # ── Создаём текстовый канал-тикет ─────────────
        safe_nick = nick.lower().replace(" ", "-")
        try:
            ticket_channel = await guild.create_text_channel(
                name=f"ticket-{safe_nick}",
                category=category,
                overwrites=overwrites,
                topic=f"📋 Заявка от {member.display_name} ({member.id}) | Ник: {nick}"
            )
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ Боту не хватает прав для создания канала.",
                ephemeral=True
            )
            log.error("❌ Нет прав для создания тикет-канала!")
            return
        except Exception as e:
            await interaction.followup.send(
                "❌ Ошибка при создании заявки. Обратись к администрации.",
                ephemeral=True
            )
            log.error(f"💥 Ошибка создания тикета: {e}")
            return

        # ── Сохраняем тикет в JSON ─────────────────────
        tickets[str(member.id)] = {
            "channel_id": ticket_channel.id,
            "nickname":   nick,
            "age":        age,
            "adequacy":   adequacy,
            "reason":     reason
        }
        _save_tickets(tickets)

        # ── Отправляем embed в тикет ───────────────────
        embed = em.embed_whitelist_ticket(nick, age, adequacy, reason, member)
        view  = TicketActionView(
            member_id=member.id,
            nickname=nick,
            channel_id=ticket_channel.id
        )

        await ticket_channel.send(
            content=f"📋 {member.mention} | 🛡️ {mod_role.mention if mod_role else ''}",
            embed=embed,
            view=view
        )

        await interaction.followup.send(
            f"✅ Заявка создана! Перейди в {ticket_channel.mention}",
            ephemeral=True
        )
        log.info(f"📋 Тикет создан: {ticket_channel.name} | {member} | ник: {nick}")


# ──────────────────────────────────────────────────────
#  🔘 VIEW — кнопка «Подать заявку»
# ──────────────────────────────────────────────────────

class WhitelistApplyView(discord.ui.View):
    """View с кнопкой подачи заявки на вайтлист."""

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="🐝 Добавиться в белый список",
        style=discord.ButtonStyle.primary,
        custom_id="whitelist_apply_btn"
    )
    async def apply_button(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        """Открываем модальное окно при нажатии."""
        # Проверка: не в вайтлисте ли уже?
        wl_role = interaction.guild.get_role(config.WHITELIST_ROLE_ID)
        if wl_role and wl_role in interaction.user.roles:
            await interaction.response.send_message(
                "✅ Ты уже в белом списке сервера!", ephemeral=True
            )
            return

        await interaction.response.send_modal(WhitelistModal())


# ──────────────────────────────────────────────────────
#  🔘 VIEW — кнопки «Принять / Отказать» в тикете
# ──────────────────────────────────────────────────────

class TicketActionView(discord.ui.View):
    """Кнопки действий в тикете для модераторов."""

    def __init__(self, member_id: int, nickname: str, channel_id: int):
        super().__init__(timeout=None)
        self.member_id  = member_id
        self.nickname   = nickname
        self.channel_id = channel_id

    def _is_moderator(self, interaction: discord.Interaction) -> bool:
        """Проверяет наличие роли модератора."""
        mod_role = interaction.guild.get_role(config.MODERATOR_ROLE_ID)
        return mod_role in interaction.user.roles if mod_role else False

    @discord.ui.button(
        label="✅ Принять",
        style=discord.ButtonStyle.success,
        custom_id="ticket_accept_btn"
    )
    async def accept_button(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        if not self._is_moderator(interaction):
            await interaction.response.send_message(
                "🛡️ Только модераторы могут использовать эту кнопку!", ephemeral=True
            )
            return

        await interaction.response.defer()

        guild      = interaction.guild
        moderator  = interaction.user
        member     = guild.get_member(self.member_id)

        if member is None:
            await interaction.followup.send(
                "❌ Пользователь не найден на сервере (возможно, покинул).", ephemeral=True
            )
            return

        # ── Выдаём роль вайтлиста ──────────────────────
        wl_role = guild.get_role(config.WHITELIST_ROLE_ID)
        if wl_role:
            try:
                await member.add_roles(wl_role, reason=f"Whitelist принят модератором {moderator}")
                log.info(f"✅ Роль вайтлиста выдана → {member}")
            except Exception as e:
                log.error(f"💥 Ошибка выдачи роли: {e}")

        # ── Команда в консольный канал ────────────────
        console_channel = guild.get_channel(config.CONSOLE_CHANNEL_ID)
        if console_channel:
            try:
                await console_channel.send(f"whitelist add {self.nickname}")
                log.info(f"💻 Отправлено в консоль: whitelist add {self.nickname}")
            except Exception as e:
                log.error(f"💥 Ошибка отправки в консоль: {e}")

        # ── Лог в лог-канал ────────────────────────────
        log_channel = guild.get_channel(config.WHITELIST_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(
                    embed=em.embed_whitelist_accepted(member, self.nickname, moderator)
                )
            except Exception as e:
                log.error(f"💥 Ошибка лога: {e}")

        # ── ЛС пользователю ────────────────────────────
        await send_safe(member, em.embed_dm_accepted())

        # ── Отключаем кнопки ──────────────────────────
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        await interaction.followup.send(
            f"✅ **{self.nickname}** добавлен в вайтлист! Роль выдана.", ephemeral=True
        )

        # ── Очищаем тикет из JSON ──────────────────────
        _remove_ticket(self.member_id)

        log.info(
            f"✅ Вайтлист принят | {member} | ник: {self.nickname} | мод: {moderator}"
        )

    @discord.ui.button(
        label="❌ Отказать",
        style=discord.ButtonStyle.danger,
        custom_id="ticket_deny_btn"
    )
    async def deny_button(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        if not self._is_moderator(interaction):
            await interaction.response.send_message(
                "🛡️ Только модераторы могут использовать эту кнопку!", ephemeral=True
            )
            return

        # Открываем Modal с причиной отказа
        await interaction.response.send_modal(
            DenyModal(
                member_id=self.member_id,
                nickname=self.nickname,
                channel_id=self.channel_id,
                parent_view=self,
                message=interaction.message
            )
        )


# ──────────────────────────────────────────────────────
#  📝 MODAL — причина отказа
# ──────────────────────────────────────────────────────

class DenyModal(discord.ui.Modal):
    """Modal для ввода причины отказа."""

    def __init__(
        self,
        member_id: int,
        nickname: str,
        channel_id: int,
        parent_view: TicketActionView,
        message: discord.Message
    ):
        super().__init__(title="❌ Причина отказа")
        self.member_id   = member_id
        self.nickname    = nickname
        self.channel_id  = channel_id
        self.parent_view = parent_view
        self.message     = message

        self.reason_input = discord.ui.InputText(
            label="📝 Укажи причину отказа",
            placeholder="Почему заявка отклонена?",
            style=discord.InputTextStyle.long,
            min_length=5,
            max_length=500
        )
        self.add_item(self.reason_input)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        guild     = interaction.guild
        moderator = interaction.user
        reason    = self.reason_input.value.strip()
        member    = guild.get_member(self.member_id)

        # ── ЛС пользователю ────────────────────────────
        if member:
            await send_safe(member, em.embed_dm_denied(reason))

        # ── Лог ────────────────────────────────────────
        log_channel = guild.get_channel(config.WHITELIST_LOG_CHANNEL_ID)
        if log_channel and member:
            try:
                await log_channel.send(
                    embed=em.embed_whitelist_denied(member, self.nickname, reason, moderator)
                )
            except Exception as e:
                log.error(f"💥 Ошибка лога отказа: {e}")

        # ── Отключаем кнопки ──────────────────────────
        for child in self.parent_view.children:
            child.disabled = True
        try:
            await self.message.edit(view=self.parent_view)
        except Exception:
            pass

        await interaction.followup.send(
            f"❌ Заявка **{self.nickname}** отклонена. Тикет удалится через "
            f"{config.TICKET_DELETE_DELAY} секунд.",
            ephemeral=True
        )

        # ── Очищаем JSON ───────────────────────────────
        _remove_ticket(self.member_id)

        log.info(
            f"❌ Вайтлист отклонён | ник: {self.nickname} | мод: {moderator} | причина: {reason}"
        )

        # ── Удаляем тикет через N секунд ──────────────
        await asyncio.sleep(config.TICKET_DELETE_DELAY)
        ticket_channel = guild.get_channel(self.channel_id)
        if ticket_channel:
            try:
                await ticket_channel.delete(reason="Заявка отклонена")
                log.info(f"🗑️ Тикет {ticket_channel.name} удалён после отказа")
            except Exception as e:
                log.error(f"💥 Ошибка удаления тикета: {e}")


# ──────────────────────────────────────────────────────
#  💾 ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ JSON
# ──────────────────────────────────────────────────────

def _load_tickets() -> dict:
    """Загружает тикеты из tickets.json."""
    try:
        with open("tickets.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_tickets(data: dict):
    """Сохраняет тикеты в tickets.json."""
    with open("tickets.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _remove_ticket(member_id: int):
    """Удаляет тикет из JSON по ID пользователя."""
    tickets = _load_tickets()
    tickets.pop(str(member_id), None)
    _save_tickets(tickets)
