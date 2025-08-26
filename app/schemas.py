from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    is_gold_related: bool
    nudge_purchase: bool
    session_id: str

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str

class PurchaseRequest(BaseModel):
    user: UserCreate
    amount: float  # Amount in INR

class PurchaseResponse(BaseModel):
    success: bool
    transaction_id: str
    gold_grams: float
    total_amount: float
    message: str
