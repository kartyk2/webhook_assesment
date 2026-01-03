from sqlalchemy import Column, String, Float, DateTime
from datetime import datetime
from .database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True, index=True)
    source_account = Column(String)
    destination_account = Column(String)
    amount = Column(Float)
    currency = Column(String)
    status = Column(String, default="PROCESSING")
    created_at = Column(DateTime, default=datetime.now)
    processed_at = Column(DateTime, nullable=True)
