from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(15), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with transactions
    transactions = relationship("Transaction", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)  # Amount in INR
    gold_grams = Column(Float, nullable=False)  # Gold purchased in grams
    gold_price_per_gram = Column(Float, nullable=False)  # Price at time of purchase
    transaction_id = Column(String(50), unique=True, nullable=False, index=True)
    status = Column(String(20), default="completed")  # completed, pending, failed
    payment_method = Column(String(50), default="digital")  # digital, upi, card
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with user
    user = relationship("User", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, user_id={self.user_id}, amount={self.amount}, gold_grams={self.gold_grams})>"

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Optional: link to user
    messages_count = Column(Integer, default=0)
    gold_interest_score = Column(Integer, default=0)
    purchase_nudged = Column(Integer, default=0)  # 0 = No, 1 = Yes
    last_activity = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ChatSession(id={self.id}, session_id='{self.session_id}', messages_count={self.messages_count})>"

class GoldPrice(Base):
    __tablename__ = "gold_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    price_per_gram = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
    source = Column(String(50), default="manual")  # manual, api, market
    is_active = Column(Integer, default=1)  # 1 = Active, 0 = Inactive
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<GoldPrice(id={self.id}, price_per_gram={self.price_per_gram}, currency='{self.currency}')>"
