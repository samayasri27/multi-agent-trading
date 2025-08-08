import logging
import datetime

class TradeExecutionAgent:
    def __init__(self, db_handler):
        self.db_handler = db_handler
        logging.basicConfig(level=logging.INFO)

    def execute_trade(self, symbol, strategy, price):
        if strategy['action'] in ['buy', 'sell']:
            quantity = strategy['quantity']
            action = strategy['action']
            reason = strategy['reason']
            
            if self.db_handler:
                self.db_handler.log_trade(symbol, action, price, quantity, reason)
            
            logging.info(f"{datetime.datetime.now()} - Executed {action} {quantity} shares of {symbol} at ${price:.2f}. Reason: {reason}")
            print(f"🔄 TRADE EXECUTED: {action.upper()} {quantity} shares of {symbol} at ${price:.2f}")
            print(f"💡 Reason: {reason}")
        else:
            logging.info(f"Holding {symbol}. Reason: {strategy.get('reason', 'No action required')}")
            print(f"⏸️ HOLDING {symbol}. Reason: {strategy.get('reason', 'No action required')}")