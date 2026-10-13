from datetime import datetime
from sqlmodel import Field, SQLModel, JSON
from typing import Any

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    vk_id: int = Field(unique=True, index=True)
    username: str
    
    is_admin: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    metadata_json: dict[str, Any] = Field(default_factory=dict, sa_type=JSON)