from typing import Optional

from pydantic import BaseModel, Field


class HeaderRequest(BaseModel):
    client_id: Optional[str] = Field(None, alias="client_id")
