# ╔══════════════════════════════════════════════════╗
# ║        📜 EMBEDS-ШАБЛОНЫ БОТА «УЛЕЙ»             ║
# ╚══════════════════════════════════════════════════╝

import discord
from datetime import datetime
import config


def _footer(embed: discord.Embed):
    """Стандартный футер для всех embed'ов."""
    embed.set_footer(text=f"🐝 {config.SERVER_NAME} • {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    return embed


# ──────────────────────────────────────────────────────
#  🐝 WHITELIST EMBEDS
# ──────────────────────────────────────────────────────

def embed_whitelist_welcome() -> discord.Embed:
    """Главный embed команды /белый_список."""
    embed = discord.Embed(
        title="🐝 Добро пожаловать на сервер «Улей»",
        description=(
            "───────────────────────────────\n"
            "📜 Тебя ещё **нет** в белом списке.\n\n"
            "Чтобы попасть на сервер — подай заявку!\n"
            "Нажми кнопку ниже и заполни форму.\n\n"
            "⚔️ **Мы ждём адекватных игроков, готовых к RP.**\n"
            "───────────────────────────────"
        ),
        color=config.COLOR_GOLD
    )
    embed.set_thumbnail(url="https://i.imgur.com/BQbBbqS.png")
    return _footer(embed)


def embed_whitelist_ticket(
    nickname: str,
    age: str,
    adequacy: str,
    reason: str,
    member: discord.Member
) -> discord.Embed:
    """Embed новой заявки в тикете."""
    embed = discord.Embed(
        title="📋 Новая заявка на вайтлист",
        color=config.COLOR_GOLD
    )
    embed.add_field(name="👤 Ник в игре", value=f"```{nickname}```", inline=True)
    embed.add_field(name="🎂 Возраст", value=f"```{age}```", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.add_field(
        name="🧠 Что для вас значит адекватность?",
        value=f"```{adequacy}```",
        inline=False
    )
    embed.add_field(
        name="🌿 Зачем вы пришли на сервер?",
        value=f"```{reason}```",
        inline=False
    )
    embed.set_author(
        name=f"{member.display_name} ({member.id})",
        icon_url=member.display_avatar.url
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    return _footer(embed)


def embed_whitelist_accepted(
    member: discord.Member,
    nickname: str,
    moderator: discord.Member
) -> discord.Embed:
    """Лог-embed об успешном принятии в вайтлист."""
    embed = discord.Embed(
        title="✅ Игрок добавлен в вайтлист",
        color=config.COLOR_GREEN
    )
    embed.add_field(name="👤 Discord", value=member.mention, inline=True)
    embed.add_field(name="🐝 Ник в игре", value=f"`{nickname}`", inline=True)
    embed.add_field(name="🛡️ Модератор", value=moderator.mention, inline=True)
    embed.set_thumbnail(url=member.display_avatar.url)
    return _footer(embed)


def embed_whitelist_denied(
    member: discord.Member,
    nickname: str,
    reason: str,
    moderator: discord.Member
) -> discord.Embed:
    """Лог-embed об отказе в вайтлисте."""
    embed = discord.Embed(
        title="❌ Заявка отклонена",
        color=config.COLOR_RED
    )
    embed.add_field(name="👤 Discord", value=member.mention, inline=True)
    embed.add_field(name="🐝 Ник", value=f"`{nickname}`", inline=True)
    embed.add_field(name="🛡️ Модератор", value=moderator.mention, inline=True)
    embed.add_field(name="📝 Причина", value=f"```{reason}```", inline=False)
    embed.set_thumbnail(url=member.display_avatar.url)
    return _footer(embed)


def embed_dm_accepted() -> discord.Embed:
    """ЛС-уведомление об одобрении заявки."""
    embed = discord.Embed(
        title="🐝 Поздравляем! Вы приняты!",
        description=(
            "───────────────────────────────\n"
            "🎉 Вы были **добавлены** в белый список сервера **«Улей»**!\n\n"
            "⚔️ Добро пожаловать в наше сообщество.\n"
            "📜 Соблюдайте правила и наслаждайтесь игрой!\n"
            "───────────────────────────────"
        ),
        color=config.COLOR_GREEN
    )
    return _footer(embed)


def embed_dm_denied(reason: str) -> discord.Embed:
    """ЛС-уведомление об отказе."""
    embed = discord.Embed(
        title="❌ Ваша заявка отклонена",
        description=(
            "───────────────────────────────\n"
            f"📝 **Причина:** {reason}\n\n"
            "Вы можете подать заявку повторно позже.\n"
            "───────────────────────────────"
        ),
        color=config.COLOR_RED
    )
    return _footer(embed)


def embed_dm_rules_passed() -> discord.Embed:
    """ЛС после прохождения теста правил."""
    embed = discord.Embed(
        title="🐝 Правила изучены!",
        description=(
            "───────────────────────────────\n"
            "📜 Вы успешно **сдали тест** по правилам сервера!\n\n"
            "Теперь вы можете подать заявку в **белый список**.\n"
            "Используйте команду `/белый_список` на сервере.\n"
            "───────────────────────────────"
        ),
        color=config.COLOR_GREEN
    )
    return _footer(embed)


# ──────────────────────────────────────────────────────
#  📰 НОВОСТИ
# ──────────────────────────────────────────────────────

def embed_news(
    title: str,
    text: str,
    author: discord.Member,
    image_url: str = None
) -> discord.Embed:
    """Embed новости сервера."""
    embed = discord.Embed(
        title=f"📰 {title}",
        description=(
            "───────────────────────────────\n"
            f"{text}\n"
            "───────────────────────────────"
        ),
        color=config.COLOR_GOLD,
        timestamp=datetime.now()
    )
    embed.set_author(
        name=f"🐝 Новости сервера «{config.SERVER_NAME}»",
        icon_url=author.display_avatar.url
    )
    embed.add_field(
        name="✍️ Автор",
        value=f"{author.mention}",
        inline=True
    )
    embed.add_field(
        name="📅 Дата",
        value=datetime.now().strftime("%d.%m.%Y"),
        inline=True
    )
    if image_url:
        embed.set_image(url=image_url)
    embed.set_footer(text=f"🐝 {config.SERVER_NAME}")
    return embed


# ──────────────────────────────────────────────────────
#  📜 ПРАВИЛА
# ──────────────────────────────────────────────────────

def embed_rules_main() -> discord.Embed:
    """Главный embed правил — вступление."""
    embed = discord.Embed(
        title="📜 ПРАВИЛА СЕРВЕРА «УЛЕЙ»",
        description=(
            "───────────────────────────────\n"
            "⚔️ **Добро пожаловать, путник!**\n\n"
            "Прежде чем вступить в наш улей,\n"
            "ознакомься с правилами сообщества.\n\n"
            "🐝 *За нарушение правил следует наказание.*\n"
            "───────────────────────────────"
        ),
        color=config.COLOR_GOLD
    )
    return _footer(embed)


def embed_rules_griefing() -> discord.Embed:
    embed = discord.Embed(
        title="⚔️ 1. Гриферство и имущество",
        color=config.COLOR_GOLD
    )
    embed.add_field(
        name="1.1 🔥 Вредительство",
        value="Запрещено **любое** проявление гриферства.\n📌 Наказание: **Бан навсегда**.",
        inline=False
    )
    embed.add_field(
        name="1.2 💰 Воровство",
        value="Запрещено брать ресурсы из **чужих сундуков**.",
        inline=False
    )
    embed.add_field(
        name="1.3 🏠 Целостность построек",
        value="Запрещено **ломать** чужие дома и сооружения.",
        inline=False
    )
    embed.add_field(
        name="1.4 🚷 Помехи игре",
        value="Запрещено **мешать** другим игрокам.",
        inline=False
    )
    return _footer(embed)


def embed_rules_chat() -> discord.Embed:
    embed = discord.Embed(
        title="💬 2. Правила чата",
        color=config.COLOR_GOLD
    )
    embed.add_field(name="2.1 🤬 Мат", value="Разрешён, но **в меру**.", inline=False)
    embed.add_field(name="2.2 🤝 Оскорбления", value="**Запрещены** личные оскорбления.", inline=False)
    embed.add_field(name="2.3 📢 Спам / Флуд", value="**Запрещён** в любом виде.", inline=False)
    embed.add_field(name="2.4 🏛️ Политика", value="Обсуждение политики **запрещено**.", inline=False)
    embed.add_field(name="2.5 📣 Реклама", value="**Запрещена** любая реклама.", inline=False)
    return _footer(embed)


def embed_rules_cheats() -> discord.Embed:
    embed = discord.Embed(
        title="🎮 3. Читы и модификации",
        color=config.COLOR_GOLD
    )
    embed.add_field(name="3.1 🚫 Читы", value="Любые читы **запрещены**.", inline=False)
    embed.add_field(name="3.2 🔍 X-Ray", value="X-Ray и аналоги **запрещены**.", inline=False)
    return _footer(embed)


def embed_rules_rp() -> discord.Embed:
    embed = discord.Embed(
        title="🎭 4. Лор и погружение (RP)",
        color=config.COLOR_GOLD
    )
    embed.add_field(name="4.1 🌍 Атмосфера", value="**Соблюдайте** атмосферу сервера.", inline=False)
    embed.add_field(name="4.2 🎭 Погружение", value="Не **разрушайте** RP намеренно.", inline=False)
    embed.add_field(name="4.3 📖 Сюжет", value="Не мешайте **сюжетным событиям**.", inline=False)
    return _footer(embed)


def embed_rules_security() -> discord.Embed:
    embed = discord.Embed(
        title="🛡️ 5. Безопасность",
        color=config.COLOR_GOLD
    )
    embed.add_field(name="5.1 🔒 Аккаунты", value="Взлом аккаунтов **запрещён**.", inline=False)
    embed.add_field(name="5.2 🕵️ Подставы", value="Подставлять других игроков **запрещено**.", inline=False)
    embed.add_field(name="5.3 👑 Администрация", value="Не тегайте администрацию **без причины**.", inline=False)
    embed.add_field(name="5.4 ⚖️ Решения", value="Администрация принимает **финальные решения**.", inline=False)
    return _footer(embed)


def embed_rules_all_list() -> list[discord.Embed]:
    """Возвращает список всех embed'ов правил."""
    return [
        embed_rules_main(),
        embed_rules_griefing(),
        embed_rules_chat(),
        embed_rules_cheats(),
        embed_rules_rp(),
        embed_rules_security(),
    ]
