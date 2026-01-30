"""Core configuration for PDF2Editable application."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # App Info
    app_name: str = "PDF2Editable"
    version: str = "0.1.0"
    debug: bool = False
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # File Processing
    max_file_size_mb: int = 150
    allowed_extensions: str = "pdf"
    file_ttl_hours: int = 1
    
    # Paths
    output_dir: Path = Path("./output")
    upload_dir: Path = Path("./uploads")
    temp_dir: Path = Path("./temp")
    
    # CORS
    allowed_origins: str = "http://localhost:3000,http://localhost:8000"
    
    @property
    def cors_origins(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    @property
    def max_file_size_bytes(self) -> int:
        """Convert MB to bytes."""
        return self.max_file_size_mb * 1024 * 1024
    
    def ensure_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        for directory in [self.output_dir, self.upload_dir, self.temp_dir]:
            directory.mkdir(parents=True, exist_ok=True)


settings = Settings()
