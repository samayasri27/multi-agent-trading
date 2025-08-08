import os
import json
import numpy as np
from datetime import datetime

class DatabaseHandler:
    def __init__(self):
        self.conn_string = os.getenv('DB_CONNECTION')
        self.use_db = False
        self.conn = None
        
        try:
            import psycopg2
            from pgvector.psycopg2 import register_vector
            self.conn = psycopg2.connect(self.conn_string)
            register_vector(self.conn)
            self.create_tables()
            self.use_db = True
        except Exception as e:
            print(f"Database not available, using in-memory storage: {e}")
            self.memory_store = []
            self.trade_logs = []

    def create_tables(self):
        if self.use_db:
            with self.conn.cursor() as cur:
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS trade_logs (
                        id SERIAL PRIMARY KEY,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        symbol TEXT,
                        action TEXT,
                        price FLOAT,
                        quantity INT,
                        reason TEXT
                    );
                ''')
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS agent_memory (
                        id SERIAL PRIMARY KEY,
                        agent_type TEXT,
                        memory_vector VECTOR(384),
                        metadata JSONB
                    );
                ''')
                self.conn.commit()

    def log_trade(self, symbol, action, price, quantity, reason):
        if self.use_db:
            with self.conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO trade_logs (symbol, action, price, quantity, reason)
                    VALUES (%s, %s, %s, %s, %s);
                ''', (symbol, action, price, quantity, reason))
                self.conn.commit()
        else:
            # Store in memory
            trade_log = {
                'timestamp': datetime.now(),
                'symbol': symbol,
                'action': action,
                'price': price,
                'quantity': quantity,
                'reason': reason
            }
            self.trade_logs.append(trade_log)
            print(f"Trade logged: {trade_log}")

    def store_memory(self, agent_type, embedding, metadata):
        if self.use_db:
            vector = np.array(embedding)
            with self.conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO agent_memory (agent_type, memory_vector, metadata)
                    VALUES (%s, %s, %s);
                ''', (agent_type, vector, json.dumps(metadata)))
                self.conn.commit()
        else:
            # Store in memory
            memory_entry = {
                'agent_type': agent_type,
                'embedding': embedding,
                'metadata': metadata
            }
            self.memory_store.append(memory_entry)

    def retrieve_memory(self, agent_type, query_embedding, limit=5):
        if self.use_db:
            vector = np.array(query_embedding)
            with self.conn.cursor() as cur:
                cur.execute('''
                    SELECT metadata FROM agent_memory
                    WHERE agent_type = %s
                    ORDER BY memory_vector <-> %s
                    LIMIT %s;
                ''', (agent_type, vector, limit))
                return [row[0] for row in cur.fetchall()]
        else:
            # Simple in-memory retrieval
            relevant_memories = [
                entry['metadata'] for entry in self.memory_store 
                if entry['agent_type'] == agent_type
            ]
            return relevant_memories[:limit]

    def close(self):
        if self.use_db and self.conn:
            self.conn.close()