from models.telemedicina_model import TelemedicinaIn, TelemedicinaOut
from db import get_connection
from fastapi import HTTPException

def cadastrar_sessao_service(sessao: TelemedicinaIn):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 1. Verifica se a consulta existe
        cursor.execute("SELECT id_consulta FROM consulta WHERE id_consulta = %s", (sessao.id_consulta,))
        consulta = cursor.fetchone()

        if not consulta:
            raise HTTPException(status_code=404, detail="Consulta não encontrada")

        # 2. Inserir a nova sessão de telemedicina
        query = """
        INSERT INTO telemedicina (id_consulta, link_video, chat, status)
        VALUES (%s, %s, %s, %s)
        """
        values = (
            sessao.id_consulta,
            str(sessao.link_video),   # Conversão correta de HttpUrl para string
            sessao.chat,
            sessao.status
        )

        cursor.execute(query, values)
        conn.commit()

        return {"mensagem": "Sessão de telemedicina cadastrada com sucesso ✅"}

    except HTTPException as e:
        raise e  # Erros HTTP são propagados
    except Exception as e:
        # Se der qualquer erro inesperado, tratamos aqui
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar sessão: {str(e)}")

def listar_sessoes_service():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_sessao, id_consulta, link_video, chat, status FROM telemedicina")
    resultados = cursor.fetchall()

    sessoes = []
    for row in resultados:
        sessao = TelemedicinaOut(
            id_sessao=row[0],
            id_consulta=row[1],
            link_video=row[2],
            chat=row[3],
            status=row[4]
        )
        sessoes.append(sessao)

    return sessoes

def encerrar_sessao_service(id_sessao: int):
    conn = get_connection()
    cursor = conn.cursor()

    # Verifica se existe
    cursor.execute("SELECT id_sessao FROM telemedicina WHERE id_sessao = %s", (id_sessao,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Sessão não encontrada")

    # Atualiza status para Encerrada
    query = """
    UPDATE telemedicina
    SET status = 'Encerrada'
    WHERE id_sessao = %s
    """
    cursor.execute(query, (id_sessao,))
    conn.commit()

    return {"mensagem": "Sessão de telemedicina encerrada ✅"}
