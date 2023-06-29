from fastapi import APIRouter, Response, status
from config.db import conn
from models.user import users
from schemas.user import User
from cryptography.fernet import Fernet
from sqlalchemy.sql import text

key = Fernet.generate_key()
f = Fernet(key)

# Crea una instancia de APIRouter llamada 'user'
user = APIRouter()


@user.get("/users", response_model=list[User], tags=["users"])
def get_users():
    # Ejecuta la consulta para obtener todos los usuarios de la base de datos
    result = conn.execute(users.select()).fetchall()

    # Convierte los objetos Row en diccionarios utilizando '_asdict()'
    result = [row._asdict() for row in result]

    # Devuelve la lista de usuarios en formato JSON
    return result


@user.get("/users/{id}", response_model=User, tags=["users"])
def get_user(id: str):
    # Ejecuta la consulta para obtener un usuario específico por su ID
    result = conn.execute(users.select().where(users.c.id == id)).first()
    if result:
        return result._asdict()
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@user.post("/users", response_model=User, tags=["users"])
def create_user(user: User):
    # Crea un nuevo usuario con los datos proporcionados
    new_user = {
        "name": user.name,
        "email": user.email,
        "password": f.encrypt(user.password.encode("utf-8"))
    }

    # Inserta el nuevo usuario en la base de datos
    conn.execute(users.insert().values(new_user))

    # Obtiene el ID del objeto insertado
    id_objeto_insertado = conn.execute(
        text("SELECT id FROM users WHERE id=LASTVAL()")).scalar()

    # Consulta el nuevo usuario por su ID
    new_user = conn.execute(users.select().where(
        users.c.id == id_objeto_insertado)).first()

    # Devuelve el nuevo usuario en formato JSON
    return new_user._asdict()


@user.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id: int):
    # Crea una cláusula WHERE para filtrar por el ID del usuario a eliminar
    where_clause = users.c.id == id

    # Ejecuta la sentencia DELETE para eliminar el usuario de la base de datos
    conn.execute(users.delete().where(where_clause))

    # Devuelve una respuesta exitosa sin contenido (204)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@user.put("/users/{id}", response_model=User, tags=["users"])
def update_user(id: int, user: User):
    # Actualiza los datos del usuario con el ID proporcionado
    conn.execute(users.update().values(name=user.name, email=user.email, password=f.encrypt(
        user.password.encode("utf-8"))).where(users.c.id == id))
    result = conn.execute(users.select().where(users.c.id == id)).first()

    return result._asdict()
