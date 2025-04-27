from db import get_connection
from models.profissionalsaude_model import ProfissionalIn, ProfissionalOut
from fastapi import HTTPException, status

def cadastrar_profissional_service(profissional: ProfissionalIn):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO usuario (login, senha, tipo_usuario)
    VALUES (%s, %s, %s)
    """
    values = (
        profissional.crm,
        profissional.senha,
        "Médico"
    )

    cursor.execute(query, values)
    id_usuario = cursor.lastrowid

    query = """
    INSERT INTO profissionalsaude (nome, crm, especialidade, telefone, email, usuario_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (
        profissional.nome,
        profissional.crm,
        profissional.especialidade,
        profissional.telefone,
        profissional.email,
        id_usuario
    )

    cursor.execute(query, values)

    query = """
    INSERT INTO administracao (id_usuario, nivel_acesso)
    VALUES (%s, %s)
    """
    values = (
        id_usuario,
        "Médio"
    )

    cursor.execute(query, values)    
    conn.commit()
    return {"mensagem": "Profissional de Saúde cadastrado com sucesso"}

def listar_profissionais_service():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profissionalsaude")
    resultados = cursor.fetchall()

    profissionais = []
    for row in resultados:
        profissional = ProfissionalOut(
            id_profissional=row[0],
            nome=row[1],
            crm=row[2],
            especialidade=row[3],
            telefone=row[4],
            email=row[5]
        )
        profissionais.append(profissional)

    return profissionais

def deletar_profissional_service(id_profissional: int):
    conn = get_connection()
    cursor = conn.cursor()

    # Verifica se o profissional existe
    cursor.execute("SELECT usuario_id FROM profissionalsaude WHERE id_profissional = %s", (id_profissional,))
    usuario_id = cursor.fetchone()
    if not usuario_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profissional de saúde não encontrado")

    usuario_id = usuario_id[0]

    # Remove o profissional
    cursor.execute("DELETE FROM profissionalsaude WHERE id_profissional = %s", (id_profissional,))
    # Remove administracao
    cursor.execute("DELETE FROM administracao ente WHERE id_usuario = %s", (usuario_id,))
    # Remove usuario
    cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (usuario_id,))
    conn.commit()

    return {"mensagem": "Profissional de saúde removido com sucesso"}

def atualizar_profissional_service(id_profissional: int, profissional_atualizar: ProfissionalIn):
    conn = get_connection()
    cursor = conn.cursor()

     # Verifica se o profissional existe
    cursor.execute("SELECT usuario_id FROM profissionalsaude WHERE id_profissional = %s", (id_profissional,))
    usuario_id = cursor.fetchone()
    if not usuario_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profissional de saúde não encontrado")

    # Atualiza os dados
    query = """
    UPDATE profissionalsaude
    SET nome = %s, crm = %s, especialidade = %s, telefone = %s, email = %s
    WHERE id_profissional = %s
    """
    values = (
        profissional_atualizar.nome,
        profissional_atualizar.crm,
        profissional_atualizar.especialidade,
        profissional_atualizar.telefone,
        profissional_atualizar.email,
        id_profissional
    )

    cursor.execute(query, values)
    
    usuario_id = usuario_id[0]

    query = """
    UPDATE usuario 
    SET senha = %s
    WHERE id_usuario = %s
    """
    values = (
        profissional_atualizar.senha,
        usuario_id
    )

    cursor.execute(query, values)

    conn.commit()
    return {"mensagem": "Profissional de saúde atualizado com sucesso"}