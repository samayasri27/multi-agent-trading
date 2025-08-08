import os
import json
from crewai import Agent
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from sentence_transformers import SentenceTransformer

class RiskManagementAgent:
    def __init__(self, db_handler):
        self.llm = ChatGroq(temperature=0.3, model_name="llama3-70b-8192", groq_api_key=os.getenv('GROQ_API_KEY'))
        self.db_handler = db_handler
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.agent = Agent(
            role='Risk Manager',
            goal='Evaluate and manage trading risks',
            backstory='Expert in risk assessment',
            llm=self.llm,
            verbose=True
        )
        self.prompt = PromptTemplate(
            input_variables=["strategy", "current_portfolio", "capital"],
            template="Evaluate risk for strategy: {strategy}. Current portfolio: {current_portfolio}, available capital: {capital}. Apply rules: stop-loss 5% below entry, max 10% capital exposure, diversify across sectors. Output JSON with 'approved' (bool), 'adjusted_strategy', 'risk_reason'."
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def evaluate_risk(self, symbol, strategy, current_portfolio, capital=100000):
        try:
            # Simplified risk evaluation to reduce token usage
            portfolio_str = f"Portfolio size: {len(current_portfolio)} positions"
            strategy_summary = f"Action: {strategy.get('action', 'hold')}, Quantity: {strategy.get('quantity', 0)}"
            
            risk_eval = self.chain.run(
                strategy=strategy_summary, 
                current_portfolio=portfolio_str, 
                capital=f"${capital:,}"
            )
            try:
                risk_data = json.loads(risk_eval)
            except:
                # Fallback risk evaluation with simple rules
                action = strategy.get('action', 'hold')
                quantity = strategy.get('quantity', 0)
                
                if action == 'hold':
                    risk_data = {'approved': True, 'adjusted_strategy': strategy, 'risk_reason': 'Hold position is safe'}
                elif action in ['buy', 'sell']:
                    # Simple risk check: limit to 10% of capital
                    max_quantity = int(capital * 0.1 / 200)  # Assuming ~$200 per share
                    if quantity > max_quantity:
                        adjusted_strategy = strategy.copy()
                        adjusted_strategy['quantity'] = max_quantity
                        risk_data = {
                            'approved': True, 
                            'adjusted_strategy': adjusted_strategy, 
                            'risk_reason': f'Quantity adjusted from {quantity} to {max_quantity} for risk management'
                        }
                    else:
                        risk_data = {'approved': True, 'adjusted_strategy': strategy, 'risk_reason': 'Risk within acceptable limits'}
                else:
                    risk_data = {'approved': False, 'adjusted_strategy': strategy, 'risk_reason': 'Unknown action type'}
        except Exception as e:
            print(f"Risk evaluation error: {e}")
            risk_data = {'approved': False, 'adjusted_strategy': strategy, 'risk_reason': 'Error in risk evaluation'}
        
        if self.db_handler:
            embedding = self.embedder.encode(str(risk_data))
            self.db_handler.store_memory('risk', embedding, {'symbol': symbol, 'risk_eval': risk_data})
        return risk_data