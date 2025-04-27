from models.consulta_model import ConsultaIn, ConsultaOut
from db import get_connection
from fastapi import HTTPException

def cadastrar_consulta_service(consulta: ConsultaIn):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO consulta (id_paciente, id_profissional, data_hora, status)
    VALUES (%s, %s, %s, %s)
    """
    values = (
        consulta.id_paciente,
        consulta.id_profissional,
        consulta.data_hora.replace("T", " "),  # Substituir 'T' por espaço no datetime
        consulta.status
    )
    cursor.execute(query, values)
    conn.commit()

    return {"mensagem": "Consulta cadastrada com sucesso ✅"}

def listar_consultas_service():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT id_consulta, id_paciente, id_profissional, data_hora, status
    FROM consulta
    """
    cursor.execute(query)
    resultados = cursor.fetchall()

    consultas = []
    for row in resultados:
        consulta = ConsultaOut(
            id_consulta=row[0],
            id_paciente=row[1],
            id_profissional=row[2],
            data_hora=row[3].strftime("%Y-%m-%dT%H:%M:%S") if row[3] else None,
            status=row[4]
        )
        consultas.append(consulta)

    return consultas

def deletar_consulta_service(id_consulta: int):
    conn = get_connection()
    cursor = conn.cursor()

    # Verifica se a consulta existe
    cursor.execute("SELECT id_consulta FROM consulta WHERE id_consulta = %s", (id_consulta,))
    consulta = cursor.fetchone()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")

    # Deleta a consulta
    query = """
    DELETE FROM consulta
    WHERE id_consulta = %s
    """
    cursor.execute(query, (id_consulta,))
    conn.commit()

    return {"mensagem": "Consulta removida com sucesso ✅"}

from models.consulta_model import ConsultaUpdate

def atualizar_consulta_service(id_consulta: int, consulta: ConsultaUpdate):
    conn = get_connection()
    cursor = conn.cursor()

    # Verifica se a consulta existe
    cursor.execute("SELECT id_consulta FROM consulta WHERE id_consulta = %s", (id_consulta,))
    consulta_existente = cursor.fetchone()
    if not consulta_existente:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")

    # Atualizar apenas os campos informados
    campos_para_atualizar = []
    valores = []

    if consulta.data_hora:
        campos_para_atualizar.append("data_hora = %s")
        valores.append(consulta.data_hora.replace("T", " "))

    if consulta.status:
        campos_para_atualizar.append("status = %s")
        valores.append(consulta.status)

    if not campos_para_atualizar:
        raise HTTPException(status_code=400, detail="Nenhum dado para atualizar enviado")

    query = f"""
    UPDATE consulta
    SET {", ".join(campos_para_atualizar)}
    WHERE id_consulta = %s
    """
    valores.append(id_consulta)

    cursor.execute(query, tuple(valores))
    conn.commit()

    return {"mensagem": "Consulta atualizada com sucesso ✅"}
