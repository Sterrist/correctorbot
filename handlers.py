from aiogram import Router, F
from aiogram.types import Message
from logging import getLogger
from corrector import OpenAICorrector
from config import settings
import re

router = Router()

corrector = OpenAICorrector(
    base_url=settings.OPENAI_BASE_URL,
    api_key=settings.OPENAI_API_KEY.get_secret_value(),
    system_prompt=settings.OPENAI_SYSTEM_PROMPT,
    model=settings.OPENAI_MODEL
)

logger = getLogger(__name__)

MODE_PATTERN = re.compile(
    r"^\.\.\.(?:\[(?P<mode>[a-z_]+)\])?\s*(?P<text>.*)$",
    re.DOTALL,
)

def parse_message(value: str) -> tuple[str | None, str] | None:
    match = MODE_PATTERN.fullmatch(value)

    if match is None:
        return None

    mode = match.group("mode")
    text = match.group("text").strip()

    if not text:
        return None

    return mode, text

@router.business_message(F.text.startswith('...'))
async def correct_message_text(m: Message):
    clear_text = m.text.removeprefix("...").lstrip()
    if not clear_text:
        return

    mode, text = parse_message(m.text)

    corrected_text = await corrector.correct_text(
        text=text,
        mode=mode
    )

    await m.edit_text(corrected_text)

    logger.info(
        "Скорректирован текст для @%s (%s)",
        m.from_user.username or m.from_user.full_name,
        m.from_user.id,
    )

@router.business_message(F.caption.startswith('...'))
async def correct_message_caption(m: Message):
    clear_text = m.caption.removeprefix("...").lstrip()
    if not clear_text:
        return

    mode, text = parse_message(m.caption)

    corrected_text = await corrector.correct_text(
        text=text,
        mode=mode
    )

    await m.edit_caption(corrected_text)

    logger.info(
        "Скорректирована подпись для @%s (%s)",
        m.from_user.username or m.from_user.full_name,
        m.from_user.id,
    )
