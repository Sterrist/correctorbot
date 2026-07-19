import re
from logging import getLogger
from aiogram import F, Router
from aiogram.types import Message
from config import settings
from corrector import OpenAICorrector

router = Router()
logger = getLogger(__name__)

corrector = OpenAICorrector(
    base_url=settings.OPENAI_BASE_URL,
    api_key=settings.OPENAI_API_KEY.get_secret_value(),
    model=settings.OPENAI_MODEL,
)

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

def get_reply_context(message: Message) -> str | None:
    replied_message = message.reply_to_message

    if replied_message is None:
        return None

    return replied_message.text or replied_message.caption

@router.business_message(F.text.startswith("..."))
async def correct_message_text(message: Message) -> None:
    parsed_message = parse_message(message.text)

    if parsed_message is None:
        return

    mode, text = parsed_message

    if not corrector.supports_mode(mode):
        logger.warning("Получен неизвестный режим: %s", mode)
        return

    corrected_text = await corrector.correct_text(
        text=text,
        mode=mode,
        context=get_reply_context(message),
    )

    await message.edit_text(
        text=corrected_text,
        parse_mode=None,
    )

    logger.info(
        "Скорректирован текст для @%s (%s)",
        message.from_user.username or message.from_user.full_name,
        message.from_user.id,
    )

@router.business_message(F.caption.startswith("..."))
async def correct_message_caption(message: Message) -> None:
    parsed_message = parse_message(message.caption)

    if parsed_message is None:
        return

    mode, text = parsed_message

    if not corrector.supports_mode(mode):
        logger.warning("Получен неизвестный режим: %s", mode)
        return

    corrected_text = await corrector.correct_text(
        text=text,
        mode=mode,
        context=get_reply_context(message),
    )

    await message.edit_caption(
        caption=corrected_text,
        parse_mode=None,
    )

    logger.info(
        "Скорректирована подпись для @%s (%s)",
        message.from_user.username or message.from_user.full_name,
        message.from_user.id,
    )
