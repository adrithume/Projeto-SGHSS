from pydantic import BaseModel

class PacienteIn(BaseModel):
    nome: str
    cpf: str
    data_nascimento: str
    telefone: str = None
    email: str = None,
    senha: str

class PacienteOut(BaseModel):
    id_paciente: int
    nome: str
    cpf: str
    data_nascimento: str
    telefone: str = None
    email: str = None