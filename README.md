# SlotLock

A meeting room booking API built to practice backend fundamentals — specifically **race conditions, database transactions, and concurrency control** — using FastAPI and PostgreSQL.

## The Idea

Rooms can be booked for a specific time window. The one rule that must never break: **two bookings for the same room can never overlap**, even if two people submit conflicting requests at the exact same moment.

The naive implementation (check for conflicts, then insert) looks correct but has a race condition — a gap between the check and the write where two overlapping bookings can both slip through. This project is built specifically to:

1. Implement the naive version
2. Prove it's broken under concurrent load
3. Fix it two different ways and compare them

## Core Concepts Practiced

- **Race conditions** — reproducing a real check-then-act bug under concurrent requests
- **Database transactions & row locking** — using `SELECT ... FOR UPDATE` to make check-and-insert atomic
- **Postgres exclusion constraints** — letting the database itself guarantee no overlapping bookings, no app-level locking required
- **Scheduled background jobs** — an auto-release job for no-shows, which creates its own miniature race between a check-in and the release sweep
- **API validation** — Pydantic schemas for request/response shapes

## Tech Stack

| Layer | Choice |
|---|---|
| Framework | FastAPI + Uvicorn |
| ORM | SQLAlchemy (+ Alembic for migrations) |
| Database | PostgreSQL (required — exclusion constraints are Postgres-only) |
| Auth | JWT (`python-jose` + `passlib`) |
| Scheduled jobs | APScheduler (in-process) |
| Testing | pytest, `httpx` async test client, `threading` for concurrency tests |
| Environment | Docker Compose (FastAPI app + Postgres) |

## Project Structure

```
slotlock/
├── app/
│   ├── main.py          # app instance, routers, startup (scheduler)
│   ├── models.py        # SQLAlchemy models: Room, Booking
│   ├── schemas.py        # Pydantic request/response models
│   ├── database.py       # engine + session setup
│   ├── jobs.py            # no-show auto-release job
│   └── routers/
│       ├── auth.py
│       ├── rooms.py
│       └── bookings.py    # the hot path — both locking approaches live here
├── tests/
│   ├── test_bookings.py
│   └── test_race_conditions.py
├── scripts/
│   └── stress_test.py     # fires concurrent overlapping bookings
├── alembic/
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## API Endpoints

| Method | Route | Description |
|---|---|---|
| POST | `/auth/register` | Create a user |
| POST | `/auth/login` | Get a JWT |
| POST | `/rooms` | Create a room |
| GET | `/rooms` | List rooms |
| GET | `/rooms/{id}/availability` | Free/busy view for a given day |
| POST | `/rooms/{id}/bookings` | Create a booking — the race-condition-prone endpoint |
| GET | `/bookings/mine` | List current user's bookings |
| DELETE | `/bookings/{id}` | Cancel a booking |
| POST | `/bookings/{id}/checkin` | Check in (feeds the no-show job) |

## Getting Started

```bash
git clone <repo-url>
cd slotlock
cp .env.example .env
docker-compose up --build
```

Once running, interactive API docs are available at `http://localhost:8000/docs`.

## Running the Stress Test

The stress test fires concurrent overlapping booking requests at the same room to reproduce the race condition:

```bash
python scripts/stress_test.py
```

Run it against the naive implementation to see double-booking happen, then against the fixed implementation to confirm it holds.

## Roadmap

- [ ] Schema, migrations, auth, room CRUD
- [ ] Naive booking endpoint + availability view
- [ ] Stress test script proving the race condition
- [ ] Fix #1: row-level locking (`SELECT ... FOR UPDATE`)
- [ ] Fix #2: Postgres exclusion constraint
- [ ] No-show auto-release job
- [ ] Stretch: recurring bookings, waitlist per room/slot

## Team

Split roughly as:
- **Person A** — auth, rooms, availability endpoint, Docker setup
- **Person B** — booking endpoint (both fix approaches), stress-test script

Each person writes concurrency tests against the *other's* booking implementation to cross-check for edge cases.