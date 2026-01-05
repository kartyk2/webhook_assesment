# webhook_assesment
webhook_assesment

---

# Transaction Webhook Service

A minimal **FastAPI** service that accepts transaction webhooks, stores them idempotently, processes them asynchronously, and exposes a status query API.

---

## 🚀 Tech Stack

* **FastAPI** – API framework
* **SQLAlchemy** – ORM
* **Pydantic** – Validation
* **Uvicorn** – ASGI server
* **SQLite** – Database

---

## ▶️ Run Locally

```bash
git clone https://github.com/<your-username>/transaction-webhook-service.git
cd transaction-webhook-service

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

uvicorn app.main:app --reload
```

Service runs at:

```
http://localhost:8000
```

---

## 🔍 API Endpoints

### Health Check

```
GET /
```

### Transaction Webhook

```
POST /v1/webhooks/transactions
```

```json
{
  "transaction_id": "tx_123",
  "source_account": "ACC_1",
  "destination_account": "ACC_2",
  "amount": 100,
  "currency": "USD"
}
```

* Idempotent (duplicates ignored)
* Returns `202 Accepted`
* Processing happens in background

---

### Transaction Status

```
GET /v1/transactions/{transaction_id}
```

---

## 🧪 Test Quickly

```bash
curl -X POST http://localhost:8000/v1/webhooks/transactions \
  -H "Content-Type: application/json" \
  -d '{ "transaction_id":"tx_123","source_account":"A","destination_account":"B","amount":100,"currency":"USD" }'
```

```bash
curl http://localhost:8000/v1/transactions/tx_123
```

Swagger UI:

```
http://localhost:8000/docs
```

---

## 🧠 Design Choices

* **FastAPI** for speed and auto-docs
* **BackgroundTasks** for non-blocking processing
* **Idempotent webhook handling** to avoid duplicates
* **Dependency-managed DB sessions** for safety
* Clean separation of API, DB, and worker logic

---

## 📌 Improvements (Future)

* Celery / queue-based processing
* Auth on webhook endpoint
* Alembic migrations
* Docker support
