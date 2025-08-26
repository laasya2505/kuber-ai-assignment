import openai
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class GoldInvestmentAssistant:
    def __init__(self):
        self.sessions = {}  # Simple in-memory session storage
        
    def analyze_message(self, message: str, session_id: str = None) -> dict:
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Initialize session
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "messages": [],
                "gold_interest_score": 0,
                "purchase_nudged": False
            }
        
        session = self.sessions[session_id]
        session["messages"].append({"role": "user", "content": message})
        
        # Check if message is gold investment related
        is_gold_related = self._is_gold_investment_query(message)
        
        if is_gold_related:
            session["gold_interest_score"] += 1
            response = self._get_gold_investment_response(message, session)
        else:
            response = "I'm sorry, I can only help you with gold investment queries. Would you like to know about the benefits of investing in digital gold?"
        
        # Check if we should nudge for purchase
        nudge_purchase = (session["gold_interest_score"] >= 2 and 
                         not session["purchase_nudged"])
        
        if nudge_purchase:
            response += "\n\n💰 Based on our conversation, you seem interested in gold investment! Would you like to purchase some digital gold right now? It's safe, secure, and you can start with as little as ₹100."
            session["purchase_nudged"] = True
        
        return {
            "response": response,
            "is_gold_related": is_gold_related,
            "nudge_purchase": nudge_purchase,
            "session_id": session_id
        }
    
    def _is_gold_investment_query(self, message: str) -> bool:
        gold_keywords = [
            "gold", "investment", "invest", "buying", "purchase", "digital gold",
            "precious metals", "portfolio", "savings", "returns", "inflation",
            "hedge", "market", "price"
        ]
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in gold_keywords)
    
    def _get_gold_investment_response(self, message: str, session: dict) -> str:
        try:
            # Enhanced context for better responses
            context = """You are Kuber AI, an expert gold investment advisor from India. You provide detailed, helpful, and encouraging advice about gold investment benefits. 

    Key points to remember:
    - Gold is an excellent hedge against inflation in India
    - Digital gold offers convenience without storage hassles
    - Indians have cultural affinity for gold
    - Current gold prices around ₹6,500 per gram
    - Digital gold is backed by physical gold in secure vaults
    - Minimum investment can be as low as ₹100
    - Provide practical, actionable advice
    - Be enthusiastic but professional
    - Give detailed explanations (150-200 words)"""
            
            messages = [
                {"role": "system", "content": context},
                {"role": "user", "content": message}
            ]
            
            response = openai.chat.completions.create(
                model="gpt-4o",  # Changed to GPT-4o
                messages=messages,
                max_tokens=250,  # Increased from 150
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            # Enhanced fallback responses
            fallback_responses = {
                "benefits": """Gold is an excellent hedge against inflation and currency devaluation! Here's why digital gold is perfect for you:

    ✨ **Inflation Protection**: Gold historically maintains purchasing power
    💰 **Easy Investment**: Start with just ₹100, no minimum limits
    🏦 **No Storage Hassles**: Your gold is safely stored in MMTC-PAMP vaults
    📱 **Instant Liquidity**: Buy/sell anytime through the app
    🇮🇳 **Perfect for Indians**: Culturally significant + financial benefits
    📈 **Portfolio Diversification**: Reduces overall investment risk

    Digital gold gives you all benefits of physical gold without the storage concerns. It's backed 1:1 by actual gold bars!""",
                
                "price": """Gold is currently trading around ₹6,500 per gram - a great entry point! Here's what makes it attractive:

    📊 **Historical Performance**: Gold has grown 8-10% annually over long term
    💹 **Current Market**: Prices are stable with upward potential
    🌍 **Global Factors**: Economic uncertainty makes gold more valuable
    💱 **Rupee Hedge**: Protects against currency depreciation
    ⏰ **Timing**: Market experts suggest gold allocation of 5-10% in portfolios

    With digital gold, you can buy fractional grams, making it affordable for everyone. No need to buy full coins or bars!""",
                
                "how": """Investing in digital gold is incredibly simple and secure! Here's the complete process:

    🔐 **What is Digital Gold**: 99.9% pure gold stored in secure MMTC-PAMP vaults
    📱 **How to Buy**: Through our app - just enter amount and confirm
    💳 **Payment**: Use UPI, cards, or net banking
    📄 **Documentation**: Get instant purchase certificate
    🏦 **Storage**: Professional vaults with insurance coverage
    💰 **Selling**: Instant sale at live market rates
    🥇 **Physical Conversion**: Convert to coins/bars if needed (min 0.5g)

    Every gram you buy is backed by actual physical gold. You own real gold, just stored digitally!""",
                
                "safe": """Absolutely! Digital gold is completely safe and regulated. Here's why you can trust it:

    🛡️ **Regulatory Backing**: Follows RBI and government guidelines
    🏦 **MMTC-PAMP Partnership**: India's premier precious metals company
    🔒 **Secure Vaults**: Your gold stored in bank-grade security facilities
    📜 **Transparency**: Real-time pricing linked to international markets
    ✅ **Purity Guarantee**: 99.9% pure gold certified
    🏢 **Insurance**: Full insurance coverage on stored gold
    📊 **Audit**: Regular third-party audits ensure gold backing

    It's as safe as keeping gold in a bank locker, but much more convenient and liquid!"""
            }
            
            message_lower = message.lower()
            if any(word in message_lower for word in ["benefit", "advantage", "why"]):
                return fallback_responses["benefits"]
            elif any(word in message_lower for word in ["price", "cost", "rate"]):
                return fallback_responses["price"]
            elif any(word in message_lower for word in ["how", "process", "buy"]):
                return fallback_responses["how"]
            elif any(word in message_lower for word in ["safe", "secure", "risk"]):
                return fallback_responses["safe"]
            else:
                return fallback_responses["benefits"]


# Global instance
llm_assistant = GoldInvestmentAssistant()
