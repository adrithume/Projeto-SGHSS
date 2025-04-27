from pydantic import BaseModel

class LoginRequest(BaseModel):
    login: str
    senha: str

class Usuario(BaseModel):
    id_usuario: int
    login: str
    tipo_usuario: str