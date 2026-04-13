import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LLM Settings
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1")
    DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    
    # Database Settings
    DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")
    POSTGRES_DB_URL = os.getenv("POSTGRES_DB_URL")
    SQLITE_DB_PATH = "ecommerce.db"
    
    @property
    def DATABASE_URI(self):
        if self.DATABASE_TYPE == "postgresql":
            if not self.POSTGRES_DB_URL:
                raise ValueError("POSTGRES_DB_URL is required when DATABASE_TYPE is postgresql")
            return self.POSTGRES_DB_URL
        return f"sqlite:///{self.SQLITE_DB_PATH}"

    # UI Settings
    APP_TITLE = "SQL AI | Enterprise Semantic Layer"
    APP_VERSION = "2.0.0"
    
    # Security Settings
    MAX_ROWS_LIMIT = 100
    FORBIDDEN_KEYWORDS = [
        "delete", "drop", "truncate", "update", "insert", 
        "alter", "grant", "revoke", "create", "exec"
    ]

config = Config()
