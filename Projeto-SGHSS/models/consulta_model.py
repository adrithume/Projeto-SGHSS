from pydantic import BaseModel

class ConsultaIn(BaseModel):
    id_paciente: int
    id_profissional: int
    data_hora: str  # formato ISO 'YYYY-MM-DDTHH:MM'
    status: str = "Agendada"  # Padrão: Agendada

class ConsultaOut(BaseModel):
    id_consulta: int
    id_paciente: int
    id_profissional: int
    data_hora: str
    status: str

class ConsultaUpdate(BaseModel):
    data_hora: str = None  # opcional
    status: str = None     # opcional