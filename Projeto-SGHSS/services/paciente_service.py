from db import get_connection
from models.paciente_model import PacienteIn, PacienteOut
from fastapi import HTTPException, status

def cadastrar_paciente_service(paciente: PacienteIn):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO usuario (login, senha, tipo_usuario)
    VALUES (%s, %s, %s)
    """
    values = (
        paciente.cpf,
        paciente.senha,
        "Paciente"
    )

    cursor.execute(query, values)
    id_usuario = cursor.lastrowid

    query = """
    INSERT INTO paciente (nome, cpf, data_nascimento, telefone, email, usuario_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (
        paciente.nome,
        paciente.cpf,
        paciente.data_nascimento,
        paciente.telefone,
        paciente.email,
        id_usuario
    )

    cursor.execute(query, values)

    query = """
    INSERT INTO administracao (id_usuario, nivel_acesso)
    VALUES (%s, %s)
    """
    values = (
        id_usuario,
        "Baixo"
    )

    cursor.execute(query, values)

    conn.commit()
    return {"mensagem": "Paciente cadastrado com sucesso"}

def listar_pacientes_service():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM paciente")
    resultados = cursor.fetchall()

    pacientes = []
    for row in resultados:
        paciente = PacienteOut(
            id_paciente=row[0],
            nome=row[1],
            cpf=row[2],
            data_nascimento=row[3].strftime("%Y-%m-%d") if row[3] else None,
            telefone=row[4],
            email=row[5]
        )
        pacientes.append(paciente)

    return pacientes

def deletar_paciente_service(id_paciente: int):
    conn = get_connection()
    cursor = conn.cursor()

    # Verifica se o paciente existe
    cursor.execute("SELECT usuario_id FROM paciente WHERE id_paciente = %s", (id_paciente,))
    usuario_id = cursor.fetchone()
    if not usuario_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")

    usuario_id = usuario_id[0]

    # Remove o paciente
    cursor.execute("DELETE FROM paciente WHERE id_paciente = %s", (id_paciente,))
    # Remove administracao
    cursor.execute("DELETE FROM administracao ente WHERE id_usuario = %s", (usuario_id,))
    # Remove usuario
    cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (usuario_id,))
    conn.commit()

    return {"mensagem": "Paciente removido com sucesso"}

def atualizar_paciente_service(id_paciente: int, paciente_atualizar: PacienteIn):
    conn = get_connection()
    cursor = conn.cursor()

     # Verifica se o paciente existe
    cursor.execute("SELECT usuario_id FROM paciente WHERE id_paciente = %s", (id_paciente,))
    usuario_id = cursor.fetchone()
    if not usuario_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")

    # Atualiza os dados
    query = """
    UPDATE paciente
    SET nome = %s, cpf = %s, data_nascimento = %s, telefone = %s, email = %s
    WHERE id_paciente = %s
    """
    values = (
        paciente_atualizar.nome,
        paciente_atualizar.cpf,
        paciente_atualizar.data_nascimento,
        paciente_atualizar.telefone,
        paciente_atualizar.email,
        id_paciente
    )

    cursor.execute(query, values)
    
    usuario_id = usuario_id[0]

    query = """
    UPDATE usuario 
    SET senha = %s
    WHERE id_usuario = %s
    """
    values = (
        paciente_atualizar.senha,
        usuario_id
    )

    cursor.execute(query, values)

    conn.commit()
    return {"mensagem": "Paciente atualizado com sucesso"}