from fastapi import Depends, FastAPI, HTTPException
# modelos
from models.usuario_model import UsuarioIn, UsuarioOut
from models.paciente_model import PacienteIn, PacienteOut
from models.profissionalsaude_model import ProfissionalIn, ProfissionalOut
from models.login_model import LoginRequest, Usuario
from models.consulta_model import ConsultaIn, ConsultaOut, ConsultaUpdate
from models.prontuario_model import ProntuarioIn, ProntuarioOut, ProntuarioUpdate
from models.telemedicina_model import TelemedicinaIn, TelemedicinaOut
from services.auth_service import verificar_token

# serviços
from services.usuario_service import cadastrar_usuario_service, listar_usuarios_service, deletar_usuario_service, atualizar_usuario_service
from services.paciente_service import cadastrar_paciente_service, listar_pacientes_service, deletar_paciente_service, atualizar_paciente_service
from services.teste_db_service import test_db_service
from services.auth_service import autenticar_usuario, criar_token_acesso, verificar_token
from services.profissionalsaude_service import cadastrar_profissional_service, deletar_profissional_service, listar_profissionais_service, atualizar_profissional_service
from services.consulta_service import cadastrar_consulta_service, listar_consultas_service, deletar_consulta_service, atualizar_consulta_service
from services.prontuario_service import cadastrar_prontuario_service, listar_prontuarios_service, atualizar_prontuario_service
from services.telemedicina_service import cadastrar_sessao_service, listar_sessoes_service, encerrar_sessao_service

app = FastAPI()

# Endpoint publico para teste de conexão db
@app.get("/test-db")
def test_db():
    try:
        result = test_db_service()
        return {"status": "Conexão bem-sucedida", "resultado": result}
    except Exception as e:
        return {"erro": str(e)}

# Endpoint para autenticação 
@app.post("/auth/login")
def login(request: LoginRequest):
    try:
        usuario = autenticar_usuario(request.login, request.senha)
        token = criar_token_acesso(usuario)
        return {"token_type": "bearer", "access_token": token}
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Erro ao fazer login:", str(e))
        raise HTTPException(status_code=500, detail="Erro interno ao fazer login")

# Endpoint para cadastrar usuario
@app.post("/usuario")
def cadastrar_usuario(usuario: UsuarioIn, payload: dict = Depends(verificar_token)):
    try:
        return cadastrar_usuario_service(usuario)
    except Exception as e:
        print("Erro ao cadastrar usuário:", str(e))
        raise HTTPException(status_code=500, detail="Erro interno ao cadastrar usuário")

# Endpoint para listar usuarios 
@app.get("/usuarios", response_model=list[UsuarioOut])
def listar_usuarios():
    try:
        return listar_usuarios_service()
    except Exception as e:
        print("Erro ao listar usuários:", str(e))
        raise HTTPException(status_code=500, detail=f"Erro interno ao listar usuários: {str(e)}")

 # Endpoint para remover usuário
@app.delete("/usuario/{id_usuario}")
def deletar_usuario(id_usuario: int):
    try:
        return deletar_usuario_service(id_usuario)
    except Exception as e:
        print("Erro ao remover usuário:", str(e))
        raise HTTPException(status_code=500, detail=f"Erro interno ao deletar usuário: {str(e)}")

 # Endpoint para atualizar usuário  
@app.put("/usuario/{id_usuario}")
def atualizar_usuario(id_usuario: int, usuario: UsuarioIn):
    try:
        return atualizar_usuario_service(id_usuario, usuario)
    except Exception as e:
        print("Erro ao atualizar usuário:", str(e))
        raise HTTPException(status_code=500, detail=f"Erro interno ao atualizar usuário: {str(e)}")

# Endpoint para cadastrar paciente
@app.post("/paciente")
def cadastrar_paciente(paciente: PacienteIn, payload: dict = Depends(verificar_token)):
    try:
        return cadastrar_paciente_service(paciente)
    except Exception as e:
        print("Erro ao cadastrar paciente:", str(e))
        raise HTTPException(status_code=500, detail="Erro interno ao cadastrar paciente")

# Endpoint: Listar todos os pacientes
@app.get("/pacientes", response_model=list[PacienteOut])
def listar_pacientes(payload: dict = Depends(verificar_token)):
    try:
         return listar_pacientes_service()    
    except Exception as e:
        print("Erro ao listar pacientes:", str(e))
        raise HTTPException(status_code=500, detail="Erro interno ao buscar pacientes")
    
 # Endpoint para remover paciente
@app.delete("/paciente/{id_paciente}")
def deletar_paciente(id_paciente: int, payload: dict = Depends(verificar_token)):
    try:
        return deletar_paciente_service(id_paciente)
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Erro ao remover paciente:", str(e))
        raise HTTPException(status_code=500, detail="Erro interno ao remover paciente")
    
# Endpoint para atualizar paciente
@app.put("/paciente/{id_paciente}")
def atualizar_paciente(id_paciente: int, paciente: PacienteIn, payload: dict = Depends(verificar_token)):
    try:
        return atualizar_paciente_service(id_paciente, paciente)
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Erro ao atualizar paciente:", str(e))
        raise HTTPException(status_code=500, detail="Erro interno ao atualizar paciente")
    
    # Endpoint para cadastrar profissional de saúde
@app.post("/profissionalsaude")
def cadastrar_profissional(profissional: ProfissionalIn, payload: dict = Depends(verificar_token)):
    try:
        return cadastrar_profissional_service(profissional)
    except Exception as e:
        print("Erro ao cadastrar profissional:", str(e))
        raise HTTPException(status_code=500, detail="Erro interno ao cadastrar profissional")
    
    # Endpoint: Listar todos os profissionais de saúde
@app.get("/profissionalsaude", response_model=list[ProfissionalOut])
def listar_profissionais(payload: dict = Depends(verificar_token)):
    try:
         return listar_profissionais_service()    
    except Exception as e:
        print("Erro ao listar profissionais de saúde:", str(e))
        raise HTTPException(status_code=500, detail="Erro interno ao buscar profissionais")
    
     # Endpoint para remover profissional de saúde
@app.delete("/profissionalsaude/{id_profissional}")
def deletar_profissional(id_profissional: int, payload: dict = Depends(verificar_token)):
    try:
        return deletar_profissional_service(id_profissional)
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Erro ao remover profissional:", str(e))
        raise HTTPException(status_code=500, detail="Erro interno ao remover profissional")
    
    # Endpoint para atualizar profissional
@app.put("/profissionalsaude/{id_profissional}")
def atualizar_profissional(id_profissional: int, profissional: ProfissionalIn, payload: dict = Depends(verificar_token)):
    try:
        return atualizar_profissional_service(id_profissional, profissional)
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Erro ao atualizar profissional de saúde:", str(e))
        raise HTTPException(status_code=500, detail="Erro interno ao atualizar profissional")

    # Endpoint para cadastrar consulta
@app.post("/consulta")
def cadastrar_consulta(consulta: ConsultaIn):
    try:
        return cadastrar_consulta_service(consulta)
    except Exception as e:
        print("Erro ao cadastrar consulta:", str(e))
        raise HTTPException(status_code=500, detail=f"Erro interno ao cadastrar consulta: {str(e)}")
    
    # Endpoint para listar consultas
@app.get("/consultas", response_model=list[ConsultaOut])
def listar_consultas():
    try:
        return listar_consultas_service()
    except Exception as e:
        print("Erro ao listar consultas:", str(e))
        raise HTTPException(status_code=500, detail=f"Erro interno ao listar consultas: {str(e)}")

    # Endpoint para deletar consultas
@app.delete("/consulta/{id_consulta}")
def deletar_consulta(id_consulta: int):
    try:
        return deletar_consulta_service(id_consulta)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao deletar consulta: {str(e)}")

    # Endpoint para atualizar data e/ou status da consulta
@app.put("/consulta/{id_consulta}")
def atualizar_consulta(id_consulta: int, consulta: ConsultaUpdate):
    try:
        return atualizar_consulta_service(id_consulta, consulta)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao atualizar consulta: {str(e)}")
    
    # Endpoint para cadastrar prontuário
@app.post("/prontuario")
def cadastrar_prontuario(prontuario: ProntuarioIn):
    try:
        return cadastrar_prontuario_service(prontuario)
    except Exception as e:
        print("Erro ao cadastrar prontuário:", str(e))
        raise HTTPException(status_code=500, detail=f"Erro interno ao cadastrar prontuário: {str(e)}")

     # Endpoint para listar prontuários
@app.get("/prontuarios", response_model=list[ProntuarioOut])
def listar_prontuarios():
    try:
        return listar_prontuarios_service()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar prontuários: {str(e)}")

    # Endpoint para que apenas médicos possam atualizar os prontuários
@app.put("/prontuario/{id_prontuario}")
def atualizar_prontuario(id_prontuario: int, prontuario: ProntuarioUpdate, token: str = Depends(verificar_token)):
    try:
        user_payload = token  # A payload contém as informações do usuário logado
        return atualizar_prontuario_service(id_prontuario, prontuario, user_payload)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar prontuário: {str(e)}")
    
# 🔹 Cadastrar nova sessão de telemedicina
@app.post("/telemedicina")
def cadastrar_sessao(sessao: TelemedicinaIn):
    return cadastrar_sessao_service(sessao)

# 🔹 Listar sessões de telemedicina
@app.get("/telemedicina", response_model=list[TelemedicinaOut])
def listar_sessoes():
    return listar_sessoes_service()

# 🔹 Encerrar uma sessão de telemedicina
@app.put("/telemedicina/{id_sessao}/encerrar")
def encerrar_sessao(id_sessao: int):
    return encerrar_sessao_service(id_sessao)
