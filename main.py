from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
app.title = "fastAPI SENA"
app.version = "2.0.0"
security = HTTPBasic()


# Modelo para el usuario
class User(BaseModel):
    id: int
    username: str
    email: str
    contraseña: str


# Modelo para actualizar un usuario
class UserUpdate(BaseModel):
    username: str
    email: str


# Base de datos temporal
fake_db = []


# Verificación básica de usuario
def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "admin"
    correct_password = "password"
    if credentials.username == correct_username and credentials.password == correct_password:
        return credentials.username
    else:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )


# Ruta GET para obtener todos los usuarios
@app.get("/cuentas", tags=["Account"])
def get_accounts():
    if not fake_db:
        return {"message": "No hay cuentas registradas."}
    return {"accounts": fake_db}


# Ruta GET para obtener un usuario por ID
@app.get("/cuentas/{user_id}", tags=["Account"])
def get_account_by_id(user_id: int):
    for user in fake_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


# Ruta POST para crear un nuevo usuario
@app.post("/create", tags=["Account"])
def create_account(user: User):
    # Verifica si el usuario ya existe
    for existing_user in fake_db:
        if existing_user["id"] == user.id:
            raise HTTPException(
                status_code=400,
                detail=f"El usuario con ID {user.id} ya existe.",
            )
    # Agrega el usuario a la base de datos temporal
    fake_db.append(user.dict())
    return {"message": "Cuenta creada exitosamente", "user": user}


# Ruta PUT para actualizar la cuenta de un usuario
@app.put("/update_account/{user_id}", tags=["Account"])
def update_account(user_id: int, user: UserUpdate):
    for existing_user in fake_db:
        if existing_user["id"] == user_id:
            existing_user["username"] = user.username
            existing_user["email"] = user.email
            return {"message": "Cuenta actualizada exitosamente", "user": existing_user}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


# Ruta DELETE para eliminar un usuario
@app.delete("/delete/{user_id}", tags=["Account"])
def delete_user(user_id: int):
    for index, user in enumerate(fake_db):
        if user["id"] == user_id:
            del fake_db[index]
            return {"message": f"Usuario con ID {user_id} de nombre eliminado exitosamente"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
