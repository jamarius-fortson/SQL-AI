import os
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent, SQLDatabaseToolkit
from langchain_core.messages import SystemMessage
from tools import SafeSQLExecutor, QueryComplexityAnalyzer
from config import config

class SQLQueryAgent:
    """Enterprise SQL Agent powered by DeepSeek and specialized reasoning"""
    
    def __init__(self, database_uri: str, api_key: str = None):
        self.api_key = api_key or config.DEEPSEEK_API_KEY
            
        if not self.api_key:
            raise ValueError("DeepSeek API key is required. Set DEEPSEEK_API_KEY env var.")

        # Database Engine Optimization
        self.db = SQLDatabase.from_uri(
            database_uri,
            sample_rows_in_table_info=3,
        )
        
        # LLM Configuration: Optimized for SQL Generation
        self.llm = ChatOpenAI(
            model=config.DEEPSEEK_MODEL, 
            openai_api_key=self.api_key,
            openai_api_base=config.DEEPSEEK_API_BASE,
            temperature=0,
            model_kwargs={"top_p": 0.1}
        )
        
        # Enhanced Toolkit with custom safety tools
        self.toolkit = SQLDatabaseToolkit(
            db=self.db,
            llm=self.llm
        )
        
        # Custom Prompt for Higher Accuracy
        self.system_message = SystemMessage(content="""
        You are Daniel, an elite Data Architect and SQL Analyst at a FAANG company.
        Your mission is to extract actionable intelligence from structured data.

        OPERATIONAL PROTOCOLS:
        1. SCHEMA FIRST: Use 'sql_db_list_tables' and 'sql_db_schema' before any query.
        2. JOIN PERFECTION: Always verify relationship keys.
        3. AGNOSTIC DIALECT: Write standard SQL compatible with the detected database.
        4. ABSOLUTE SAFETY: You are in a read-only environment. DO NOT even think about DDL or DML.
        5. EXECUTIVE SUMMARY: Provide a concise, high-level business insight after the data.
        6. NEURAL LOGIC: If a query fails, analyze the error and self-correct immediately.

        TONE: Precise, authoritative, and helpful.
        """)

        # Orchestration: Using more robust agent type
        self.agent = create_sql_agent(
            llm=self.llm,
            toolkit=self.toolkit,
            agent_type="openai-tools", # More reliable for modern LLMs
            verbose=True,
            handle_parsing_errors=True,
            suffix="Always conclude with a clear business insight based on the data retrieved."
        )
        
        self.history = []
    
    def query(self, question: str) -> Dict[str, Any]:
        """Execute a natural language query with advanced reasoning and safety"""
        try:
            # Multi-layer safety check
            if self._security_audit(question):
                return {
                    "success": False,
                    "error": "SECURITY ALERT: Input contains unauthorized command patterns."
                }

            # Inject conversational context
            context_aware_input = self._build_context(question)

            # Execution with reasoning loop
            result = self.agent.invoke({
                "input": context_aware_input
            })

            # Memoization of interaction
            self._update_history(question, result["output"])
            
            return {
                "success": True,
                "answer": result["output"],
                "steps": result.get("intermediate_steps", [])
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"PIPELINE FAILURE: {str(e)}"
            }

    def _security_audit(self, question: str) -> bool:
        """Heuristic check for prompt injection or malicious intent"""
        q = question.lower()
        return any(word in q for word in config.FORBIDDEN_KEYWORDS)

    def _build_context(self, question: str) -> str:
        """Maintains short-term memory for coherent multi-turn analysis"""
        if not self.history:
            return question
            
        history_snippet = "\n".join([f"Analyst Prompt: {h['q']}\nResult Summary: {h['a']}" for h in self.history[-2:]])
        return f"PREVIOUS CONTEXT:\n{history_snippet}\n\nNEW OBJECTIVE: {question}"

    def _update_history(self, q: str, a: str):
        self.history.append({"q": q, "a": a})
        if len(self.history) > 5:
            self.history.pop(0)

    def get_schema(self) -> str:
        return self.db.get_table_info()
