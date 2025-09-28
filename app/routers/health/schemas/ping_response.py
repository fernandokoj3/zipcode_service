from pydantic import BaseModel, Field


class PingResponse(BaseModel):
    """Resposta ao ping da aplicação"""

    pong: bool = Field(..., title="Resposta do ping")
    version: str = Field(..., title="Versão da aplicação")
