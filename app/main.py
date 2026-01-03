from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from .database import SessionLocal, engine
from .models import Transaction
from .schema import TransactionWebhook, TransactionResponse
from .worker import process_transaction
from .database import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- Health Check ----------------
@app.get("/")
def health_check():
    return {"status": "HEALTHY", "current_time": datetime.utcnow().isoformat() + "Z"}


# ---------------- Webhook ----------------
@app.post("/v1/webhooks/transactions", status_code=202)
def receive_webhook(
    payload: TransactionWebhook,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    tx = db.query(Transaction).filter_by(transaction_id=payload.transaction_id).first()

    if tx:
        return

    tx = Transaction(
        transaction_id=payload.transaction_id,
        source_account=payload.source_account,
        destination_account=payload.destination_account,
        amount=payload.amount,
        currency=payload.currency,
        status="PROCESSING",
    )

    db.add(tx)
    db.commit()

    background_tasks.add_task(process_transaction, db, payload.transaction_id)
    return


# ---------------- Status Query ----------------
@app.get("/v1/transactions/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: str, db: Session = Depends(get_db)):
    tx = db.query(Transaction).filter_by(transaction_id=transaction_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx
