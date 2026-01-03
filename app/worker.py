import time
from datetime import datetime
from sqlalchemy.orm import Session
from .models import Transaction

def process_transaction(db: Session, transaction_id: str):
    time.sleep(30)  # simulate external API

    tx = db.query(Transaction).filter_by(transaction_id=transaction_id).first()
    if tx and tx.status != "PROCESSED":
        tx.status = "PROCESSED"
        tx.processed_at = datetime.utcnow()
        db.commit()
