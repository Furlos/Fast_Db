from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создаем экземпляр FastAPI
app = FastAPI()

# Создаем базовую модель для SQLAlchemy
Base = declarative_base()

# Создаем модель пользователя
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String)

# Создаем базу данных SQLite
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Создаем сессию для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Модель для передачи данных о пользователе при создании или обновлении
class UserCreateUpdate(BaseModel):
    username: str
    email: str

# Маршрут для создания пользователя
@app.post("/users/")
def create_user(user: UserCreateUpdate):
    db = SessionLocal()
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user

# Маршрут для получения пользователя по ID
@app.get("/users/{user_id}")
def read_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

# Маршрут для обновления пользователя по ID
@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserCreateUpdate):
    db = SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        db.close()
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user

# Маршрут для удаления пользователя по ID
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    db = SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        db.close()
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    db.delete(db_user)
    db.commit()
    db.close()
    return {"message": "Пользователь успешно удален"}