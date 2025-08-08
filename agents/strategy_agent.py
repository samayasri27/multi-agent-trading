import os
import pandas as pd
from crewai import Agent
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from sentence_transformers import SentenceTransformer
import json

class StrategyAgent:
    def __init__(self, db_handler):
        self.llm = ChatGroq(temperature=0.7, model_name="llama3-70b-8192", groq_api_key=os.getenv('GROQ_API_KEY'))
        self.db_handler = db_handler
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.agent = Agent(
            role='Strategy Generator',
            goal='Generate trading strategies based on data and sentiment',
            backstory='Expert in trading strategies',
            llm=self.llm,
            verbose=True
        )
        self.prompt = PromptTemplate(
            input_variables=["market_data", "sentiment", "indicators"],
            template="Generate a trading strategy for the stock based on market data: {market_data}, sentiment: {sentiment}, and indicators: {indicators}. Output as JSON with 'action' (buy/sell/hold), 'quantity', 'reason'."
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def compute_indicators(self, data):
        try:
            # For single data point, use the current price as moving averages
            current_price = data['close'].iloc[0]
            indicators = {
                'SMA_5': current_price,  # Use current price as proxy
                'SMA_20': current_price * 0.98,  # Slightly lower for demo
                'RSI': 50,  # Neutral RSI
                'current_price': current_price,
                'volume': data['volume'].iloc[0]
            }
            return indicators
        except Exception as e:
            print(f"Error computing indicators: {e}")
            return {
                'SMA_5': 100,
                'SMA_20': 98,
                'RSI': 50,
                'current_price': 100,
                'volume': 1000000
            }

    def generate_strategy(self, symbol, market_data, sentiment):
        try:
            indicators = self.compute_indicators(market_data)
            price = market_data['close'].iloc[0]
            volume = market_data['volume'].iloc[0]
            
            # Enhanced strategy logic with multiple factors
            strategy_data = self._generate_enhanced_strategy(symbol, price, volume, sentiment, indicators)
            
        except Exception as e:
            print(f"Strategy generation error: {e}")
            # Fallback to basic strategy
            strategy_data = self._generate_basic_strategy(sentiment)
        
        if self.db_handler:
            embedding = self.embedder.encode(str(strategy_data))
            self.db_handler.store_memory('strategy', embedding, {'symbol': symbol, 'strategy': strategy_data})
        return strategy_data
    
    def _generate_enhanced_strategy(self, symbol, price, volume, sentiment, indicators):
        """Generate strategy based on multiple factors"""
        
        # Technical analysis factors
        high_volume = volume > 500000
        
        # Price momentum (simplified)
        price_momentum = 'neutral'
        if price > 200:  # High price stocks
            price_momentum = 'strong' if high_volume else 'moderate'
        elif price > 100:  # Mid price stocks
            price_momentum = 'moderate'
        else:  # Low price stocks
            price_momentum = 'weak'
        
        # Decision matrix based on sentiment and technical factors
        if sentiment['sentiment'] == 'positive' and sentiment['score'] > 0.5:
            if price_momentum == 'strong':
                return {'action': 'buy', 'quantity': 15, 'reason': f'Strong positive sentiment ({sentiment["score"]:.2f}) + strong momentum'}
            elif price_momentum == 'moderate':
                return {'action': 'buy', 'quantity': 10, 'reason': f'Positive sentiment ({sentiment["score"]:.2f}) + moderate momentum'}
            else:
                return {'action': 'buy', 'quantity': 5, 'reason': f'Positive sentiment ({sentiment["score"]:.2f}) but weak momentum'}
                
        elif sentiment['sentiment'] == 'negative' and sentiment['score'] > 0.5:
            if price_momentum == 'strong':
                return {'action': 'sell', 'quantity': 8, 'reason': f'Strong negative sentiment ({sentiment["score"]:.2f}) + strong momentum'}
            elif price_momentum == 'moderate':
                return {'action': 'sell', 'quantity': 5, 'reason': f'Negative sentiment ({sentiment["score"]:.2f}) + moderate momentum'}
            else:
                return {'action': 'hold', 'quantity': 0, 'reason': f'Negative sentiment ({sentiment["score"]:.2f}) but weak momentum - wait'}
                
        else:  # Neutral sentiment
            if price_momentum == 'strong' and high_volume:
                return {'action': 'buy', 'quantity': 8, 'reason': 'Strong technical momentum despite neutral sentiment'}
            elif price < 150 and high_volume:  # Value opportunity
                return {'action': 'buy', 'quantity': 12, 'reason': 'Potential value opportunity with high volume'}
            elif price > 400:  # High price, be cautious
                return {'action': 'sell', 'quantity': 3, 'reason': 'Taking profits at high price levels'}
            else:
                return {'action': 'hold', 'quantity': 0, 'reason': 'Neutral conditions - monitoring market'}
    
    def _generate_basic_strategy(self, sentiment):
        """Basic fallback strategy"""
        if sentiment['sentiment'] == 'positive' and sentiment['score'] > 0.4:
            return {'action': 'buy', 'quantity': 8, 'reason': 'Basic positive sentiment strategy'}
        elif sentiment['sentiment'] == 'negative' and sentiment['score'] > 0.4:
            return {'action': 'sell', 'quantity': 4, 'reason': 'Basic negative sentiment strategy'}
        else:
            return {'action': 'hold', 'quantity': 0, 'reason': 'Basic neutral strategy'}