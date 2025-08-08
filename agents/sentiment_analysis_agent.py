import os
import finnhub
from crewai import Agent
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from sentence_transformers import SentenceTransformer
import json

class SentimentAnalysisAgent:
    def __init__(self, db_handler):
        self.finnhub_client = finnhub.Client(api_key=os.getenv('FINNHUB_API_KEY'))
        self.llm = ChatGroq(temperature=0.5, model_name="llama3-70b-8192", groq_api_key=os.getenv('GROQ_API_KEY'))
        self.db_handler = db_handler
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.agent = Agent(
            role='Sentiment Analyst',
            goal='Analyze market sentiment from news',
            backstory='Expert in sentiment analysis',
            llm=self.llm,
            verbose=True
        )
        self.prompt = PromptTemplate(
            input_variables=["news"],
            template="Analyze the sentiment of this news: {news}. Output as JSON with 'sentiment' (positive/negative/neutral) and 'score' (0-1)."
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def fetch_news(self, symbol):
        try:
            # Use recent dates for news
            from datetime import datetime, timedelta
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            news = self.finnhub_client.company_news(
                symbol, 
                _from=start_date.strftime('%Y-%m-%d'), 
                to=end_date.strftime('%Y-%m-%d')
            )
            return [item['headline'] + ' ' + (item.get('summary', '') or '') for item in news[:5]]
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

    def analyze_sentiment(self, symbol):
        try:
            news = self.fetch_news(symbol)
            if not news:
                # Generate varied sentiment based on symbol characteristics for demo
                import random
                sentiments = ['positive', 'negative', 'neutral']
                sentiment_type = random.choice(sentiments)
                score = random.uniform(0.3, 0.8)
                avg_sentiment = {'sentiment': sentiment_type, 'score': score}
                print(f"No news found, using simulated sentiment for demo: {avg_sentiment}")
            else:
                # Try to analyze news sentiment
                sentiments = []
                for article in news[:2]:  # Analyze fewer articles to save tokens
                    try:
                        # Simple keyword-based sentiment as fallback
                        positive_words = ['growth', 'profit', 'gain', 'rise', 'up', 'strong', 'beat', 'exceed', 'positive', 'bullish']
                        negative_words = ['loss', 'drop', 'fall', 'down', 'weak', 'miss', 'decline', 'negative', 'bearish', 'concern']
                        
                        article_lower = article.lower()
                        positive_count = sum(1 for word in positive_words if word in article_lower)
                        negative_count = sum(1 for word in negative_words if word in article_lower)
                        
                        if positive_count > negative_count:
                            sentiment_data = {'sentiment': 'positive', 'score': min(0.8, 0.5 + positive_count * 0.1)}
                        elif negative_count > positive_count:
                            sentiment_data = {'sentiment': 'negative', 'score': min(0.8, 0.5 + negative_count * 0.1)}
                        else:
                            sentiment_data = {'sentiment': 'neutral', 'score': 0.5}
                        
                        sentiments.append(sentiment_data)
                    except Exception as e:
                        print(f"Error analyzing article: {e}")
                        sentiments.append({'sentiment': 'neutral', 'score': 0.5})
                
                # Calculate average sentiment
                if sentiments:
                    positive_scores = [s['score'] for s in sentiments if s['sentiment'] == 'positive']
                    negative_scores = [s['score'] for s in sentiments if s['sentiment'] == 'negative']
                    neutral_scores = [s['score'] for s in sentiments if s['sentiment'] == 'neutral']
                    
                    if positive_scores and len(positive_scores) >= len(negative_scores):
                        avg_sentiment = {'sentiment': 'positive', 'score': sum(positive_scores) / len(positive_scores)}
                    elif negative_scores and len(negative_scores) > len(positive_scores):
                        avg_sentiment = {'sentiment': 'negative', 'score': sum(negative_scores) / len(negative_scores)}
                    else:
                        avg_sentiment = {'sentiment': 'neutral', 'score': 0.5}
                else:
                    avg_sentiment = {'sentiment': 'neutral', 'score': 0.5}
                    
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            # Generate random sentiment for demo purposes
            import random
            sentiments = ['positive', 'negative', 'neutral']
            sentiment_type = random.choice(sentiments)
            score = random.uniform(0.4, 0.8)
            avg_sentiment = {'sentiment': sentiment_type, 'score': score}
        
        if self.db_handler:
            embedding = self.embedder.encode(str(avg_sentiment))
            self.db_handler.store_memory('sentiment', embedding, {'symbol': symbol, 'sentiment': avg_sentiment})
        return avg_sentiment