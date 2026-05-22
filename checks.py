# ╔══════════════════════════════════════════════════╗
# ║         🛡️ ПРОВЕРКИ ПРАВ «УЛЕЙ»                  ║
# ╚══════════════════════════════════════════════════╝

import discord
from discord.ext import commands
import config
from logger import log


def is_moderator():
    """
    Декоратор-проверка: имеет ли пользователь роль модератора.
    Используется в slash-командах через @checks.is_moderator()
    """
    async def predicate(ctx: discord.ApplicationContext) -> bool:
        if ctx.guild is None:
            await ctx.respond(
                "❌ Эта команда доступна только на сервере!", ephemeral=True
            )
            return False

        mod_role = ctx.guild.get_role(config.MODERATOR_ROLE_ID)
        if mod_role is None:
            log.warning(f"⚠️ Роль модератора {config.MODERATOR_ROLE_ID} не найдена!")
            await ctx.respond(
                "❌ Роль модератора не настроена. Обратитесь к администратору.",
                ephemeral=True
            )
            return False

        if mod_role not in ctx.author.roles:
            await ctx.respond(
                "🛡️ У вас нет прав для использования этой команды!",
                ephemeral=True
            )
            log.warning(
                f"🚫 {ctx.author} попытался использовать команду без прав мода."
            )
            return False

        return True

    return commands.check(predicate)


async def member_has_whitelist_role(member: discord.Member) -> bool:
    """Проверяет, есть ли у участника роль вайтлиста."""
    role = member.guild.get_role(config.WHITELIST_ROLE_ID)
    return role in member.roles if role else False


async def check_channel_exists(guild: discord.Guild, channel_id: int) -> bool:
    """Проверяет, существует ли канал на сервере."""
    channel = guild.get_channel(channel_id)
    if channel is None:
        log.error(f"❌ Канал {channel_id} не найден на сервере {guild.name}!")
        return False
    return True


async def send_safe(member: discord.Member, embed: discord.Embed) -> bool:
    """
    Безопасная отправка в ЛС. Возвращает True при успехе, False если ЛС закрыты.
    """
    try:
        await member.send(embed=embed)
        log.info(f"📬 ЛС отправлено → {member} ({member.id})")
        return True
    except discord.Forbidden:
        log.warning(f"📪 Не удалось отправить ЛС → {member} (ЛС закрыты)")
        return False
    except Exception as e:
        log.error(f"💥 Ошибка отправки ЛС → {member}: {e}")
        return False
