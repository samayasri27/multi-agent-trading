import os
import yfinance as yf
import finnhub
import pandas as pd
import requests
from crewai import Agent
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from sentence_transformers import SentenceTransformer

class MarketDataAgent:
    def __init__(self, db_handler):
        self.finnhub_client = finnhub.Client(api_key=os.getenv('FINNHUB_API_KEY'))
        self.llm = ChatGroq(temperature=0, model_name="llama3-70b-8192", groq_api_key=os.getenv('GROQ_API_KEY'))
        self.db_handler = db_handler
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.agent = Agent(
            role='Market Data Analyst',
            goal='Fetch and process real-time market data',
            backstory='Expert in financial data processing',
            llm=self.llm,
            verbose=True
        )
        self.prompt = PromptTemplate(
            input_variables=["data"],
            template="Process this market data: {data} and provide key insights."
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def fetch_stock_data(self, symbol):
        try:
            # Try Finnhub first as it's more reliable
            quote = self.finnhub_client.quote(symbol)
            if quote and quote.get('c', 0) > 0:
                combined = pd.DataFrame({
                    'open': [quote['o']],
                    'high': [quote['h']],
                    'low': [quote['l']],
                    'close': [quote['c']],
                    'volume': [1000000]  # Default volume
                })
                return combined
        except Exception as e:
            print(f"Finnhub error: {e}")
        
        try:
            # Fallback to yfinance
            session = requests.Session()
            session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
            ticker = yf.Ticker(symbol, session=session)
            data = ticker.history(period="5d")  # Get more days to ensure data
            if not data.empty:
                latest = data.iloc[-1]
                combined = pd.DataFrame({
                    'open': [latest['Open']],
                    'high': [latest['High']],
                    'low': [latest['Low']],
                    'close': [latest['Close']],
                    'volume': [latest['Volume']]
                })
                return combined
        except Exception as e:
            print(f"YFinance error: {e}")
        
        # Fallback with mock data for demo purposes
        print(f"Using mock data for {symbol}")
        return pd.DataFrame({
            'open': [150.0],
            'high': [155.0],
            'low': [148.0],
            'close': [152.5],
            'volume': [1000000]
        })

    def process_data(self, symbol):
        data = self.fetch_stock_data(symbol)
        # Simplified insights to reduce token usage
        price = data['close'].iloc[0]
        volume = data['volume'].iloc[0]
        insights = f"Current price: ${price:.2f}, Volume: {volume:,}"
        
        if self.db_handler:
            embedding = self.embedder.encode(insights)
            self.db_handler.store_memory('market_data', embedding, {'symbol': symbol, 'insights': insights})
        return insights
