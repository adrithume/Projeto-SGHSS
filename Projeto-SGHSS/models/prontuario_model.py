from pydantic import BaseModel

class ProntuarioIn(BaseModel):
    id_paciente: int
    id_profissional: int
    diagnostico: str
    receita: str = None
    observacoes: str = None

class ProntuarioOut(BaseModel):
    id_prontuario: int
    id_paciente: int
    id_profissional: int
    diagnostico: str
    receita: str = None
    observacoes: str = None

class ProntuarioUpdate(BaseModel):
    diagnostico: str = None
    receita: str = None
    observacoes: str = None