# ╔══════════════════════════════════════════════════╗
# ║      📜 VIEWS ПРАВИЛ И ТЕСТА «УЛЕЙ»              ║
# ╚══════════════════════════════════════════════════╝

import discord
import embeds as em
from checks import send_safe
from logger import log


# ──────────────────────────────────────────────────────
#  📋 ВОПРОСЫ ТЕСТА
# ──────────────────────────────────────────────────────

QUIZ_QUESTIONS = [
    {
        "question": "⚔️ Что будет за гриферство на сервере?",
        "options":  [
            ("🟡 Предупреждение", False),
            ("🔴 Бан навсегда",   True),
            ("🟠 Мут на 1 час",   False),
            ("🟢 Ничего",         False),
        ]
    },
    {
        "question": "💰 Можно ли брать ресурсы из чужих сундуков?",
        "options":  [
            ("✅ Да, если не закрыт",   False),
            ("❌ Нет, это запрещено",    True),
            ("🟡 Да, но не более 10",    False),
            ("🟠 Только с разрешения",   False),
        ]
    },
    {
        "question": "🎮 Какие читы разрешены на сервере?",
        "options":  [
            ("🔍 X-Ray для руды",              False),
            ("⚡ SpeedHack",                   False),
            ("❌ Никакие читы не разрешены",   True),
            ("🛡️ Только оборонительные",      False),
        ]
    },
    {
        "question": "🗣️ Что запрещено в чате?",
        "options":  [
            ("😂 Шутки и юмор",              False),
            ("📣 Спам, реклама, политика",   True),
            ("🎭 RP-диалоги",                False),
            ("❓ Вопросы к игрокам",          False),
        ]
    },
    {
        "question": "🎭 Что нужно соблюдать в RP?",
        "options":  [
            ("🌍 Атмосферу и погружение",    True),
            ("💬 Только свой ник",           False),
            ("🚀 Скорость игры",             False),
            ("🏆 Только побеждать",          False),
        ]
    }
]

import config


# ──────────────────────────────────────────────────────
#  🔘 VIEW — кнопка «Сдать правила»
# ──────────────────────────────────────────────────────

class RulesView(discord.ui.View):
    """View с кнопкой начала теста по правилам."""

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="📘 Сдать правила",
        style=discord.ButtonStyle.primary,
        custom_id="rules_quiz_start_btn",
        emoji="📘"
    )
    async def start_quiz(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        """Начинает тест по правилам."""
        view  = QuizView(member=interaction.user, question_index=0, correct_count=0)
        embed = view.make_embed()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        log.info(f"📘 {interaction.user} начал тест по правилам")


# ──────────────────────────────────────────────────────
#  🧠 КНОПКА ОДНОГО ОТВЕТА
# ──────────────────────────────────────────────────────

class AnswerButton(discord.ui.Button):
    """Кнопка одного варианта ответа в тесте."""

    def __init__(self, label: str, is_correct: bool, quiz_view: "QuizView", index: int):
        super().__init__(
            label=label,
            style=discord.ButtonStyle.secondary,
            custom_id=f"quiz_ans_{quiz_view.question_index}_{index}"
        )
        self.is_correct = is_correct
        self.quiz_view  = quiz_view

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.quiz_view.member.id:
            await interaction.response.send_message(
                "❌ Это не твой тест!", ephemeral=True
            )
            return
        await self.quiz_view.handle_answer(interaction, self.is_correct)


# ──────────────────────────────────────────────────────
#  🧠 VIEW — тест по правилам
# ──────────────────────────────────────────────────────

class QuizView(discord.ui.View):
    """Динамический тест по правилам с кнопками-ответами."""

    def __init__(self, member: discord.Member, question_index: int, correct_count: int):
        super().__init__(timeout=120)
        self.member         = member
        self.question_index = question_index
        self.correct_count  = correct_count

        question = QUIZ_QUESTIONS[question_index]
        for i, (label, is_correct) in enumerate(question["options"]):
            self.add_item(AnswerButton(label, is_correct, self, i))

    def make_embed(self) -> discord.Embed:
        """Создаёт embed текущего вопроса."""
        q_data = QUIZ_QUESTIONS[self.question_index]
        total  = len(QUIZ_QUESTIONS)

        embed = discord.Embed(
            title=f"📜 Тест по правилам — Вопрос {self.question_index + 1}/{total}",
            description=(
                "───────────────────────────────\n"
                f"❓ **{q_data['question']}**\n"
                "───────────────────────────────\n"
                "*Выбери правильный ответ:*"
            ),
            color=config.COLOR_GOLD
        )
        embed.set_footer(
            text=f"🐝 Улей • Вопрос {self.question_index + 1} из {total}"
        )
        return embed

    async def handle_answer(self, interaction: discord.Interaction, is_correct: bool):
        """Обрабатывает выбор ответа."""
        new_correct = self.correct_count + (1 if is_correct else 0)
        next_index  = self.question_index + 1
        total       = len(QUIZ_QUESTIONS)
        result_text = "✅ Правильно!" if is_correct else "❌ Неверно!"

        # Отключаем кнопки текущего вопроса
        for child in self.children:
            child.disabled = True

        if next_index >= total:
            # ── Тест завершён ─────────────────────────
            await self._finish_quiz(interaction, new_correct, result_text)
        else:
            # ── Следующий вопрос ──────────────────────
            feedback = discord.Embed(
                description=f"{result_text} Следующий вопрос...",
                color=0x2ECC71 if is_correct else 0xE74C3C
            )
            await interaction.response.edit_message(embed=feedback, view=self)

            next_view  = QuizView(self.member, next_index, new_correct)
            next_embed = next_view.make_embed()
            await interaction.followup.send(embed=next_embed, view=next_view, ephemeral=True)

    async def _finish_quiz(
        self,
        interaction: discord.Interaction,
        correct_count: int,
        last_result: str
    ):
        """Обрабатывает завершение теста."""
        total  = len(QUIZ_QUESTIONS)
        passed = correct_count >= 4  # Нужно минимум 4/5

        if passed:
            color = 0x2ECC71
            title = "🏆 Тест пройден!"
            desc  = (
                "───────────────────────────────\n"
                f"✅ {last_result}\n\n"
                f"🎉 Правильных ответов: **{correct_count}/{total}**\n\n"
                "📬 Мы отправили тебе инструкцию в личные сообщения!\n"
                "───────────────────────────────"
            )
            await send_safe(self.member, em.embed_dm_rules_passed())
            log.info(f"✅ {self.member} прошёл тест ({correct_count}/{total})")
        else:
            color = 0xE74C3C
            title = "❌ Тест провален"
            desc  = (
                "───────────────────────────────\n"
                f"❌ {last_result}\n\n"
                f"😔 Правильных ответов: **{correct_count}/{total}** (нужно минимум 4)\n\n"
                "📜 Перечитай правила и попробуй снова!\n"
                "───────────────────────────────"
            )
            log.info(f"❌ {self.member} провалил тест ({correct_count}/{total})")

        result_embed = discord.Embed(title=title, description=desc, color=color)
        result_embed.set_footer(text="🐝 Улей • Тест завершён")

        # Отключаем кнопки и показываем результат
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(embed=result_embed, view=self)
