from models.prontuario_model import ProntuarioIn, ProntuarioOut, ProntuarioUpdate
from db import get_connection
from fastapi import HTTPException, status

def cadastrar_prontuario_service(prontuario: ProntuarioIn):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO prontuario (id_paciente, id_profissional, diagnostico, receita, observacoes)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        prontuario.id_paciente,
        prontuario.id_profissional,
        prontuario.diagnostico,
        prontuario.receita,
        prontuario.observacoes
    )
    cursor.execute(query, values)

    conn.commit()

    return {"mensagem": "Prontuário cadastrado com sucesso ✅"}

    # Função para listar os prontuários cadastrados
def listar_prontuarios_service():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT id_prontuario, id_paciente, id_profissional, diagnostico, receita, observacoes
    FROM prontuario
    """
    cursor.execute(query)
    resultados = cursor.fetchall()

    prontuarios = []
    for row in resultados:
        prontuario = ProntuarioOut(
            id_prontuario=row[0],
            id_paciente=row[1],
            id_profissional=row[2],
            diagnostico=row[3],
            receita=row[4],
            observacoes=row[5]
        )
        prontuarios.append(prontuario)

    return prontuarios

def atualizar_prontuario_service(
    id_prontuario: int,
    dados: ProntuarioUpdate,
    user_payload: dict
):
    # Controle de acesso: só médicos podem atualizar
    if user_payload.get("tipo_usuario") != "Médico":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso proibido. Apenas médicos podem atualizar prontuários"
        )

    conn = get_connection()
    cursor = conn.cursor()

    # Verifica existência do prontuário
    cursor.execute(
        "SELECT id_prontuario FROM prontuario WHERE id_prontuario = %s",
        (id_prontuario,)
    )
    if not cursor.fetchone():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prontuário não encontrado"
        )

    # Monta lista de campos para atualizar
    campos = []
    valores = []
    if dados.diagnostico is not None:
        campos.append("diagnostico = %s")
        valores.append(dados.diagnostico)
    if dados.receita is not None:
        campos.append("receita = %s")
        valores.append(dados.receita)
    if dados.observacoes is not None:
        campos.append("observacoes = %s")
        valores.append(dados.observacoes)

    if not campos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum dado para atualizar enviado"
        )

    # Executa o UPDATE
    query = (
        f"UPDATE prontuario SET {', '.join(campos)} WHERE id_prontuario = %s"
    )
    valores.append(id_prontuario)
    cursor.execute(query, tuple(valores))
    conn.commit()

    return {"mensagem": "Prontuário atualizado com sucesso ✅"}