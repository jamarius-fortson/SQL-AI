import sqlalchemy
import pandas as pd
import re
from typing import Optional, List, Any
from langchain.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr
from config import config

class SQLQueryInput(BaseModel):
    """Input for SQL Query Tool"""
    query: str = Field(description="SQL query to execute. Must be a SELECT statement.")

class SafeSQLExecutor(BaseTool):
    name: str = "sql_executor"
    description: str = f"""
    Execute SQL SELECT queries on the database.
    
    CRITICAL RULES:
    - Only SELECT queries are allowed.
    - Queries are automatically limited to {config.MAX_ROWS_LIMIT} rows for safety.
    - Use this for data retrieval after confirming table names via schema_inspector.
    """
    args_schema: Any = SQLQueryInput
    db_uri: str = Field(description="Database URI")
    
    _engine: Any = PrivateAttr()

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._engine = sqlalchemy.create_engine(self.db_uri)
    
    def _run(self, query: str) -> str:
        """Execute SQL query safely and return formatted results"""
        try:
            # Clean and validate query
            clean_query = query.strip().strip("`").strip("'")
            
            if not self._is_safe_query(clean_query):
                return "SECURITY ERROR: Unauthorized query pattern detected. Only SELECT operations are permitted."
            
            # Enforce limits
            final_query = self._enforce_safety_limits(clean_query)
            
            with self._engine.connect() as conn:
                df = pd.read_sql(sqlalchemy.text(final_query), conn)
                
                if df.empty:
                    return "Zero results returned for the specified criteria."
                
                # Format for agent consumption
                return self._format_output(df)
                
        except Exception as e:
            return f"EXECUTION ERROR: {str(e)}"
    
    def _is_safe_query(self, query: str) -> bool:
        """Advanced security validation using regex and keyword auditing"""
        query_upper = query.upper()
        
        # Must start with SELECT or WITH (for CTEs)
        if not (query_upper.startswith('SELECT') or query_upper.startswith('WITH')):
            return False
            
        # Audit for destructive verbs
        for word in config.FORBIDDEN_KEYWORDS:
            # Use regex to find whole words only to avoid false positives (e.g., 'updated_at')
            pattern = rf"\b{word.upper()}\b"
            if re.search(pattern, query_upper):
                return False
        
        return True
    
    def _enforce_safety_limits(self, query: str) -> str:
        """Inject LIMIT if missing or exceeding maximum threshold"""
        query = query.rstrip('; \n')
        
        limit_match = re.search(r'LIMIT\s+(\d+)', query, re.IGNORECASE)
        if limit_match:
            requested_limit = int(limit_match.group(1))
            if requested_limit > config.MAX_ROWS_LIMIT:
                # Override excessive limits
                query = re.sub(r'LIMIT\s+\d+', f'LIMIT {config.MAX_ROWS_LIMIT}', query, flags=re.IGNORECASE)
        else:
            query += f' LIMIT {config.MAX_ROWS_LIMIT}'
            
        return query
    
    def _format_output(self, df: pd.DataFrame) -> str:
        """Convert DataFrame to a compact, agent-friendly string representation"""
        rows = len(df)
        cols = ", ".join(df.columns)
        preview = df.to_string(index=False, max_rows=20)
        return f"Results Found: {rows}\nColumns: {cols}\n\nData Preview:\n{preview}"

class QueryComplexityAnalyzer(BaseTool):
    name: str = "query_analyzer"
    description: str = "Pre-execution analysis to identify performance bottlenecks and query complexity."
    
    def _run(self, query: str) -> str:
        query_upper = query.upper()
        score = 0
        feedback = []
        
        # Complexity heuristics
        joins = query_upper.count("JOIN")
        subqueries = query_upper.count("(SELECT")
        aggregations = any(x in query_upper for x in ["GROUP BY", "SUM(", "AVG(", "COUNT("])
        
        score += (joins * 2) + (subqueries * 3) + (1 if aggregations else 0)
        
        if joins > 2: feedback.append(f"Multiple joins ({joins}) detected.")
        if subqueries > 0: feedback.append("Nested logic (subqueries) present.")
        if "SELECT *" in query_upper: feedback.append("Broad select (*) used; consider column projection.")
        
        risk = "LOW" if score < 5 else "MEDIUM" if score < 10 else "HIGH"
        
        return f"Complexity: {score} | Risk: {risk}\nInsights: {'; '.join(feedback) if feedback else 'Optimal query structure.'}"

class SchemaInspector(BaseTool):
    name: str = "schema_inspector"
    description: str = "Retrieve detailed metadata about the database tables, relations, and column types."
    db_uri: str = Field(description="Database URI")

    def _run(self, tool_input: str = "") -> str:
        from langchain_community.utilities import SQLDatabase
        db = SQLDatabase.from_uri(self.db_uri, sample_rows_in_table_info=2)
        return db.get_table_info()
