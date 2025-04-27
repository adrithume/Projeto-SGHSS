from pydantic import BaseModel

class UsuarioIn(BaseModel):
    login: str
    senha: str
    tipo_usuario: str
    nivel_acesso: str

class UsuarioOut(BaseModel):
    login: str
    tipo_usuario: str
    nivel_acesso: str