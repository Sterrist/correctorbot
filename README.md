# Corrector BOT

Небольшой Telegram бот, который исправляет грамматику, орфографию и пунктуацию в исходящих сообщениях с помощью OpenAI API.

Бот редактирует сообщение на месте и старается сохранить исходный смысл, стиль и тон текста.

## Использование

Добавьте в начало сообщения три точки:

```text
...привет отправь пожалуйста документы до завтра
```

После обработки сообщение будет заменено на исправленную версию:

```text
Привет! Отправь, пожалуйста, документы до завтра.
```

Поддерживаются обычные текстовые сообщения и подписи к медиа.

## Требования

- Python 3.12+
- Telegram-бот, подключённый к вашему аккаунту через функционал "Чат-боты"
- OpenAI API key
- Docker и Docker Compose — необязательно

## Настройка

Создайте файл `.env` в корне проекта:

```dotenv
BOT_TOKEN=your_telegram_bot_token
ADMIN_IDS=[123456789]

OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-5.4-nano-2026-03-17
```

`ADMIN_IDS` содержит Telegram ID пользователей, которым разрешено использовать бота.

## Запуск через uv

Установите зависимости:

```bash
uv sync
```

Запустите бота:

```bash
uv run python run.py
```

## Запуск через Docker Compose

```bash
docker compose -f docker-compose.without-dokploy.yml up -d --build
```

Просмотр логов:

```bash
docker compose -f docker-compose.without-dokploy.yml logs -f
```

Остановка:

```bash
docker compose -f docker-compose.without-dokploy.yml down
```

## Конфиденциальность

Текст сообщений отправляется в OpenAI API для обработки. Не используйте бота для паролей, API-ключей и другой чувствительной информации.

## Лицензия

Проект распространяется под лицензией MIT.