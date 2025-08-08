#!/usr/bin/env python3
"""
AI-Powered Multi-Agent Trading System - Main Application

This is the main entry point for the multi-agent trading system.
It orchestrates 5 specialized AI agents to analyze market data,
sentiment, generate strategies, manage risk, and execute trades.

Features:
- Real-time market data analysis
- AI-powered sentiment analysis
- Intelligent strategy generation
- Comprehensive risk management
- Automated trade execution

Author: Your Name
License: MIT
"""

import os
from dotenv import load_dotenv
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["OTEL_SDK_DISABLED"] = "true"  # Disable OpenTelemetry
from crewai import Crew, Process, Task

load_dotenv()
from database import DatabaseHandler
from agents.market_data_agent import MarketDataAgent
from agents.sentiment_analysis_agent import SentimentAnalysisAgent
from agents.strategy_agent import StrategyAgent
from agents.risk_management_agent import RiskManagementAgent
from agents.trade_execution_agent import TradeExecutionAgent
import json

def main():
    try:
        # Try to initialize database, but continue without it if it fails
        try:
            db_handler = DatabaseHandler()
            print("✓ Database connected successfully")
        except Exception as e:
            print(f"⚠ Database connection failed: {e}")
            print("Continuing without database storage...")
            db_handler = None
        
        symbol = 'AAPL'
        current_portfolio = {'AAPL': 100, 'GOOGL': 50}
        capital = 100000

        print(f"\n🚀 Starting trading analysis for {symbol}")
        print(f"Portfolio: {current_portfolio}")
        print(f"Available Capital: ${capital:,}")

        # Initialize agents
        market_agent = MarketDataAgent(db_handler)
        sentiment_agent = SentimentAnalysisAgent(db_handler)
        strategy_agent = StrategyAgent(db_handler)
        risk_agent = RiskManagementAgent(db_handler)
        execution_agent = TradeExecutionAgent(db_handler)

        # Step 1: Get market data
        print("\n📊 Fetching market data...")
        market_data = market_agent.fetch_stock_data(symbol)
        market_insights = market_agent.process_data(symbol)
        print(f"Market Data: {market_data.to_dict('records')[0]}")

        # Step 2: Analyze sentiment
        print("\n📰 Analyzing market sentiment...")
        sentiment_result = sentiment_agent.analyze_sentiment(symbol)
        print(f"Sentiment: {sentiment_result}")

        # Step 3: Generate strategy
        print("\n🎯 Generating trading strategy...")
        strategy = strategy_agent.generate_strategy(symbol, market_data, sentiment_result)
        print(f"Strategy: {strategy}")

        # Step 4: Risk evaluation
        print("\n⚖️ Evaluating risk...")
        risk_eval = risk_agent.evaluate_risk(symbol, strategy, current_portfolio, capital)
        print(f"Risk Evaluation: {risk_eval}")

        # Step 5: Execute trade if approved
        print("\n💼 Trade execution decision...")
        if risk_eval.get('approved', False):
            price = market_data['close'].iloc[-1]
            adjusted_strategy = risk_eval.get('adjusted_strategy', strategy)
            execution_agent.execute_trade(symbol, adjusted_strategy, price)
            print("✅ Trade executed successfully!")
        else:
            print(f"❌ Trade not approved: {risk_eval.get('risk_reason', 'Unknown reason')}")

        if db_handler:
            db_handler.close()
            
    except Exception as e:
        print(f"❌ Error in main execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()