from db import get_connection
from models.usuario_model import UsuarioIn, UsuarioOut
from fastapi import HTTPException, status

def cadastrar_usuario_service(usuario: UsuarioIn):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO usuario (login, senha, tipo_usuario)
    VALUES (%s, %s, %s)
    """
    values = (
        usuario.login,
        usuario.senha,
        usuario.tipo_usuario,
    )

    cursor.execute(query, values)
    id_usuario = cursor.lastrowid

    query = """
    INSERT INTO administracao (id_usuario, nivel_acesso)
    VALUES (%s, %s)
    """
    values = (
        id_usuario,
        usuario.nivel_acesso
    )

    cursor.execute(query, values)

    conn.commit()
    return {"mensagem": "Usuário cadastrado com sucesso"}

def listar_usuarios_service():
    conn = get_connection()
    cursor = conn.cursor()

    # Buscar dados de usuario + administração
    query = """
    SELECT u.id_usuario, u.login, u.tipo_usuario, a.nivel_acesso
    FROM usuario u
    JOIN administracao a ON u.id_usuario = a.id_usuario
    """
    cursor.execute(query)
    resultados = cursor.fetchall()

    usuarios = []
    for row in resultados:
        usuario = UsuarioOut(
            id_usuario=row[0],
            login=row[1],
            tipo_usuario=row[2],
            nivel_acesso=row[3]
        )
        usuarios.append(usuario)

    return usuarios

def deletar_usuario_service(id_usuario: int):
    conn = get_connection()
    cursor = conn.cursor()

    # Primeiro remover da administração
    query_admin = """
    DELETE FROM administracao
    WHERE id_usuario = %s
    """
    cursor.execute(query_admin, (id_usuario,))

    # Depois remover da tabela usuario
    query_usuario = """
    DELETE FROM usuario
    WHERE id_usuario = %s
    """
    cursor.execute(query_usuario, (id_usuario,))

    conn.commit()

    return {"mensagem": "Usuário removido com sucesso ✅"}

def atualizar_usuario_service(id_usuario: int, usuario: UsuarioIn):
    conn = get_connection()
    cursor = conn.cursor()

    # Atualizar dados do usuário
    query_usuario = """
    UPDATE usuario
    SET login = %s, senha = %s, tipo_usuario = %s
    WHERE id_usuario = %s
    """
    values_usuario = (
        usuario.login,
        usuario.senha,
        usuario.tipo_usuario,
        id_usuario
    )
    cursor.execute(query_usuario, values_usuario)

    # Atualizar nível de acesso na administração
    query_admin = """
    UPDATE administracao
    SET nivel_acesso = %s
    WHERE id_usuario = %s
    """
    values_admin = (
        usuario.nivel_acesso,
        id_usuario
    )
    cursor.execute(query_admin, values_admin)

    conn.commit()

    return {"mensagem": "Usuário atualizado com sucesso ✅"}