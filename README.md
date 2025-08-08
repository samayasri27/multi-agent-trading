# 🤖 AI-Powered Multi-Agent Trading System

A sophisticated AI-powered trading system built with **CrewAI framework** that uses multiple specialized agents to analyze market data, sentiment, and execute intelligent trading decisions. This project demonstrates advanced concepts in multi-agent systems, financial analysis, and AI-driven decision making.

## 🎯 Project Overview

This system simulates a professional trading environment where multiple AI agents collaborate to make informed trading decisions:

- **Real-time market data analysis** from multiple sources
- **AI-powered sentiment analysis** of financial news
- **Intelligent strategy generation** using LLMs
- **Comprehensive risk management** with position sizing
- **Automated trade execution** with detailed logging
- **Vector database storage** for agent memory and learning

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Market Data    │    │   Sentiment     │    │   Strategy      │
│     Agent       │───▶│   Analysis      │───▶│   Generation    │
│                 │    │     Agent       │    │     Agent       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │  Risk Management│    │ Trade Execution │
│   + pgvector    │◀───│     Agent       │◀───│     Agent       │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🤖 AI Agents

### 1. 📊 Market Data Agent
- Fetches real-time stock data from **Finnhub** and **Yahoo Finance**
- Processes market indicators and technical analysis
- Handles API failures with intelligent fallbacks

### 2. 📰 Sentiment Analysis Agent
- Analyzes financial news using **NLP** and **LLMs**
- Generates sentiment scores for market conditions
- Uses keyword analysis and AI-powered classification

### 3. 🧠 Strategy Generation Agent
- Creates trading strategies using **Groq LLM**
- Combines sentiment analysis with technical indicators
- Implements multi-factor decision matrix

### 4. ⚖️ Risk Management Agent
- Evaluates trading risks and position sizing
- Implements stop-loss and diversification rules
- Adjusts strategies based on portfolio and capital

### 5. 💼 Trade Execution Agent
- Executes approved trades with detailed logging
- Calculates trade values and portfolio impact
- Maintains comprehensive audit trail

## 🚀 Key Features

- ✅ **Multi-Agent Collaboration**: 5 specialized AI agents working together
- ✅ **Real-Time Data Integration**: Live market data from multiple APIs
- ✅ **AI-Powered Decision Making**: LLM-based strategy generation
- ✅ **Advanced Risk Management**: Portfolio optimization and position sizing
- ✅ **Vector Database Storage**: PostgreSQL with pgvector for agent memory
- ✅ **Fallback Mechanisms**: Graceful handling of API failures
- ✅ **Comprehensive Logging**: Detailed trade execution and decision tracking
- ✅ **Educational Value**: Demonstrates real-world trading concepts

## 📋 Prerequisites

- **Python 3.8+**
- **PostgreSQL 13+** with pgvector extension (optional)
- **API Keys**: Finnhub, Groq
- **Virtual Environment** (recommended)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-trading-system.git
cd ai-trading-system
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup
```bash
cp .env.sample .env
# Edit .env with your API keys
```

### 5. Database Setup (Optional)
```bash
# Install PostgreSQL and pgvector
brew install postgresql pgvector  # macOS
# or
sudo apt-get install postgresql postgresql-contrib  # Ubuntu

# Create database
createdb trading_db
psql trading_db -c "CREATE EXTENSION vector;"
```

## 🔑 API Keys Required

### Finnhub API (Free Tier Available)
1. Visit [Finnhub.io](https://finnhub.io/)
2. Sign up for free account
3. Get API key from dashboard

### Groq API (Free Tier Available)
1. Visit [Groq Console](https://console.groq.com/)
2. Create account and generate API key
3. Free tier includes generous token limits

## 🏃‍♂️ Usage

### Basic Usage
```bash
# Activate virtual environment
source venv/bin/activate

# Run the main trading system
python main.py
```

## 📊 Sample Output

```
🚀 Starting trading analysis for AAPL
Portfolio: {'AAPL': 100, 'GOOGL': 50}
Available Capital: $100,000

📊 Fetching market data...
💹 Current Price: $211.18
🔍 Market Insights: Current price: $211.18, Volume: 1,000,000

📰 Analyzing market sentiment...
😊 Sentiment: POSITIVE (Score: 0.75)

🎯 Generating trading strategy...
📋 Strategy: BUY 15 shares
💭 Reasoning: Strong positive sentiment (0.75) + strong momentum

⚖️ Evaluating risk...
✅ RISK APPROVED
🔧 Strategy adjusted: BUY 12 shares
📝 Risk Reason: Quantity adjusted for risk management

💼 Trade execution...
🔄 TRADE EXECUTED: BUY 12 shares of AAPL at $211.18
💡 Reason: Strong positive sentiment + strong momentum
💵 Trade Value: $2,534.16
✅ Trade executed successfully!
```

## 🔧 Configuration

### Risk Management Rules
- **Maximum Exposure**: 10% of capital per trade
- **Stop Loss**: 5% below entry price
- **Position Sizing**: Based on volatility and sentiment
- **Portfolio Diversification**: Across sectors and assets

### Supported Assets
- Any stock symbol supported by Finnhub/Yahoo Finance
- Examples: AAPL, GOOGL, MSFT, TSLA, AMZN, NVDA

## 📁 Project Structure

```
ai-trading-system/
├── main.py                          # Main application entry point
├── database.py                      # Database handler with fallbacks
├── demo.py                          # Interactive demo scenarios
├── test_trading_system.py           # Comprehensive test suite
├── quick_test.py                    # Quick decision testing
├── requirements.txt                 # Python dependencies
├── .env.sample                      # Sample environment variables
├── agents/
│   ├── market_data_agent.py         # Market data fetching & analysis
│   ├── sentiment_analysis_agent.py  # News sentiment analysis
│   ├── strategy_agent.py            # AI-powered strategy generation
│   ├── risk_management_agent.py     # Risk evaluation & management
│   └── trade_execution_agent.py     # Trade execution & logging
├── docs/
│   ├── TRADING_IMPROVEMENTS.md      # System improvements documentation
│   └── FIXES_SUMMARY.md             # Technical fixes summary
└── README.md                        # This file
```

## 🧪 Testing

The project includes comprehensive testing:

- **Unit Tests**: Individual agent functionality
- **Integration Tests**: Multi-agent workflows
- **Scenario Tests**: Different market conditions
- **Error Handling Tests**: API failures and edge cases

```bash
# Run all tests
python test_trading_system.py

# Test specific scenarios
python demo.py

# Quick functionality check
python quick_test.py
```

## 🔍 Technical Highlights

### AI/ML Technologies
- **CrewAI Framework**: Multi-agent orchestration
- **Groq LLM**: Fast inference for strategy generation
- **Sentence Transformers**: Text embeddings for memory
- **NLP**: Sentiment analysis and text processing

### Data & APIs
- **Finnhub API**: Professional financial data
- **Yahoo Finance**: Backup market data source
- **PostgreSQL + pgvector**: Vector database for AI memory
- **Real-time Processing**: Live market data integration

### Software Engineering
- **Error Handling**: Comprehensive fallback mechanisms
- **Logging**: Detailed execution tracking
- **Modular Design**: Separate agent responsibilities
- **Configuration Management**: Environment-based setup

## 🚨 Disclaimer

**This is a demonstration system for educational and portfolio purposes only.**

- ⚠️ **Not for actual trading**: Do not use with real money
- 📚 **Educational purpose**: Demonstrates AI and trading concepts
- 🧪 **Simulation only**: Uses paper trading simulation
- 💡 **Learning tool**: For understanding multi-agent systems

## Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) for the multi-agent framework
- [Finnhub](https://finnhub.io/) for financial data API
- [Groq](https://groq.com/) for fast LLM inference
- [PostgreSQL](https://www.postgresql.org/) and [pgvector](https://github.com/pgvector/pgvector) for vector database
