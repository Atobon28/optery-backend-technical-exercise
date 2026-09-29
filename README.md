# Optery Senior Backend Engineer — Technical Exercise

This repository contains a small backend service used for a live technical screen.

## Candidate instructions

You are joining a backend team and inheriting an unfamiliar service.

The service receives removal requests, stores them, and processes them through a simulated external provider.

Your goals during the interview are to:

1. Get the project running locally.
2. Understand the existing workflow.
3. Investigate correctness, reliability, and performance issues.
4. Make the most important fixes you identify.
5. Explain your reasoning and trade-offs as you work.

Please think out loud. You do not need to rewrite the application.

## Run

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m app.seed
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

Useful endpoints:

- `GET /health`
- `POST /removal-requests`
- `POST /removal-requests/{request_id}/process`
- `GET /removal-requests/{request_id}`
- `GET /removal-requests`

## Tests

```bash
pytest -q
```

## Interview rules

- Live coding.
- No AI assistance.
- You may use the language/runtime documentation available locally or in your editor.
- Ask clarifying questions when needed.
