from pydantic import BaseModel, HttpUrl
from typing import Optional

class TelemedicinaIn(BaseModel):
    id_consulta: int
    link_video: HttpUrl  # Validação de URL automática
    chat: Optional[str] = None  # Chat começa vazio
    status: Optional[str] = "Ativa"  # Default Ativa

class TelemedicinaOut(BaseModel):
    id_sessao: int
    id_consulta: int
    link_video: HttpUrl
    chat: Optional[str] = None
    status: str
