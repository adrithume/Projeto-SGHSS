from datetime import datetime, timedelta
from jose import jwt, JWTError
from db import get_connection
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models.login_model import Usuario
import os

# Chave secreta para assinar os tokens
SECRET_KEY = "bbef8f87c0d746f1b84f3562e15af9da9c42eb5cda63abf26c5b546cb0fe61f5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verificar_senha(plain_password, hashed_password):
    return plain_password == hashed_password

def autenticar_usuario(login: str, senha: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_usuario, login, senha, tipo_usuario FROM usuario WHERE login = %s", (login,))
    resultado = cursor.fetchone()

    if not resultado:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="login ou senha inválidos")

    id_usuario, login_db, senha_hash, tipo_usuario = resultado

    if not verificar_senha(senha, senha_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="login ou senha inválidos")

    return Usuario(id_usuario=id_usuario, login=login_db, tipo_usuario=tipo_usuario)

def criar_token_acesso(usuario: Usuario):
    expira = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "exp": expira,
        "sub": usuario.login,
        "id_usuario": usuario.id_usuario,
        "tipo_usuario": usuario.tipo_usuario
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Define onde o token será esperado
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verificar_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não autorizado: token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        return payload
    except JWTError:
        raise credentials_exception