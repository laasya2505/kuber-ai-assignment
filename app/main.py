from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Transaction  # Import from models.py now
from app.schemas import ChatRequest, ChatResponse, PurchaseRequest, PurchaseResponse
from app.llm_service import llm_assistant
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Kuber AI Gold Investment Assistant", 
    description="AI-powered gold investment chatbot and purchase system",
    version="1.0.0"
)

# API 1: Chat with Gold Investment Assistant
@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_with_assistant(request: ChatRequest):
    """
    Chat with Kuber AI about gold investments
    """
    try:
        result = llm_assistant.analyze_message(request.message, request.session_id)
        
        return ChatResponse(
            response=result["response"],
            is_gold_related=result["is_gold_related"],
            nudge_purchase=result["nudge_purchase"],
            session_id=result["session_id"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

# API 2: Purchase Digital Gold
@app.post("/api/v2/purchase", response_model=PurchaseResponse)
async def purchase_gold(request: PurchaseRequest, db: Session = Depends(get_db)):
    """
    Purchase digital gold
    """
    try:
        # Get gold price
        gold_price_per_gram = float(os.getenv("GOLD_PRICE_PER_GRAM", 6500))
        
        # Calculate gold grams
        gold_grams = request.amount / gold_price_per_gram
        
        # Create or get user
        existing_user = db.query(User).filter(User.email == request.user.email).first()
        if existing_user:
            user = existing_user
        else:
            user = User(
                name=request.user.name,
                email=request.user.email,
                phone=request.user.phone
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Create transaction
        transaction_id = f"TXN{uuid.uuid4().hex[:8].upper()}"
        
        transaction = Transaction(
            user_id=user.id,
            amount=request.amount,
            gold_grams=round(gold_grams, 4),
            gold_price_per_gram=gold_price_per_gram,
            transaction_id=transaction_id,
            status="completed"
        )
        
        db.add(transaction)
        db.commit()
        
        return PurchaseResponse(
            success=True,
            transaction_id=transaction_id,
            gold_grams=round(gold_grams, 4),
            total_amount=request.amount,
            message=f"🎉 Congratulations! You've successfully purchased {round(gold_grams, 4)} grams of digital gold for ₹{request.amount}"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing purchase: {str(e)}")

# Utility endpoints for demo
@app.get("/api/v1/transactions/{transaction_id}")
async def get_transaction(transaction_id: str, db: Session = Depends(get_db)):
    """Get transaction details"""
    transaction = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return {
        "transaction_id": transaction.transaction_id,
        "amount": transaction.amount,
        "gold_grams": transaction.gold_grams,
        "status": transaction.status,
        "created_at": transaction.created_at
    }

@app.get("/api/v1/users/{user_id}/transactions")
async def get_user_transactions(user_id: int, db: Session = Depends(get_db)):
    """Get all transactions for a user"""
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    return transactions

@app.get("/")
async def root():
    return {"message": "Kuber AI Gold Investment Assistant API is running!", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
