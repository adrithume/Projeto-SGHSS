from pydantic import BaseModel

class ProfissionalIn(BaseModel):
    nome: str
    crm: str
    especialidade: str
    telefone: str = None
    email: str = None,
    senha: str

class ProfissionalOut(BaseModel):
    id_profissional: int
    nome: str
    crm: str
    especialidade: str
    telefone: str = None
    email: str = None