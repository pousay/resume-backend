# Resume Backend

The backend service powering the contact/guestbook form on [my CV website soon](https://github.com/pousay) — a small FastAPI app that receives a name + message, stores it, and forwards a formatted notification straight to Telegram.

> This is the API only. The frontend (a React + TypeScript blueprint-themed CV) lives in a separate, private repository.

## How it works

1. A visitor submits the guestbook form on the CV site.
2. `POST /api/contacts/contact` validates the payload, stores it in SQLite, and captures the requester's IP + User-Agent.
3. A background task formats the entry as an HTML message and pushes it to a Telegram chat via the Bot API, with automatic retries (up to 5 attempts) on failure.
4. The API responds immediately — the visitor doesn't wait on the Telegram round-trip.

## Tech stack

- **[FastAPI](https://fastapi.tiangolo.com/)** — async web framework
- **[SQLAlchemy 2.0](https://www.sqlalchemy.org/)** — ORM, using the modern `Mapped[]` declarative style
- **[Pydantic v2](https://docs.pydantic.dev/) / pydantic-settings** — request validation & typed environment config
- **[SlowAPI](https://github.com/laurents/slowapi)** — rate limiting (per-IP)
- **[httpx](https://www.python-httpx.org/)** — async HTTP client for the Telegram Bot API
- **SQLite** — zero-config storage for contact submissions
- **flake8** — linting

## Project structure

```
app/
├── config/          # settings (env vars) and rate-limiter setup
├── database/        # SQLAlchemy base + engine/session
├── dependencies/     # FastAPI dependency-injected DB session & notifier
├── models/          # Pydantic request models
├── routes/          # API route handlers (create / retrieve)
├── schema/          # SQLAlchemy ORM models
├── services/        # Telegram client + notification orchestration
└── main.py          # app entrypoint, CORS, router wiring
```

## API endpoints

All routes are mounted under `/api/contacts`.

#### CAUTION! 
**GET METHODS HAVE BEEN ADDED FOR TESTING, YOU SHALL REMOVE THEM ON PRODUCTION**

| Method | Path                     | Description                                  |
| ------ | ------------------------ | --------------------------------------------- |
| `POST` | `/contact`               | Create a new contact/guestbook entry. Rate-limited to 1 request/minute per IP. |
| `GET`  | `/contacts`               | List all stored contact entries.              |
| `GET`  | `/contacts/{contact_id}`  | Retrieve a single contact entry by ID.         |

### `POST /api/contacts/contact`

**Request body**

```json
{
  "name": "Jane Doe",
  "message": "Loved the floor-plan CV — the lightning animation is a nice touch!"
}
```

**Response `201 Created`**

```json
{
  "message": "Contact created successfully",
  "id": 1
}
```

## Getting started

### Prerequisites

- Python 3.11+
- A Telegram bot token and target chat ID (see below)

### Setup

```bash
git clone https://github.com/pousay/resume-backend.git
cd resume-backend

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Environment variables

Copy `.env.example` to `.env` and fill in your own values:

```dotenv
DATABASE_URL = "sqlite:///./contacts.db"
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID_HERE"
```

| Variable             | Description                                                                 |
| --------------------- | ---------------------------------------------------------------------------- |
| `DATABASE_URL`        | SQLAlchemy connection string (SQLite by default, no extra setup needed).      |
| `TELEGRAM_BOT_TOKEN`  | Token for a bot created via [@BotFather](https://t.me/BotFather).             |
| `TELEGRAM_CHAT_ID`    | The chat/user ID that should receive new-contact notifications.               |

### Run the dev server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

### Linting

```bash
flake8
```

## Notes on CORS

`app/main.py` currently allows all origins (`allow_origins=["*"]`) for ease of local development. If you deploy this yourself, you'll likely want to lock this down to your actual frontend's origin.

## License

This project is provided as-is for personal/portfolio use. Feel free to reference it, but please don't republish it as your own.