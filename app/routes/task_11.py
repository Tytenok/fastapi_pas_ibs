from fastapi import Body, Path, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

router = APIRouter(tags=["SQLalchemy"])

# База данных SQLAlchemy
engine = create_engine("sqlite:///mydatabase.db", echo=True)
Base = declarative_base()


# Определение модели пользователя для Pydantic
class UserSQL(BaseModel):
    id: int
    name: str
    email: str


# Определение модели пользователя для SQLAlchemy
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(120), nullable=False, unique=True)


# Создание таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Получение сессии базы данных
SessionLocal = scoped_session(sessionmaker(bind=engine))


def get_db():
    """
    Функция для получения сессии базы данных.
    Returns:
        Session: Сессия базы данных SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# a. Добавление строки в таблицу Users
@router.post("/users/", response_model=UserSQL)
async def create_user(user: UserSQL):
    db: Session = next(get_db())
    new_user = User(id=user.id, name=user.name, email=user.email)
    try:
        db.add(new_user)
        db.commit()
        return new_user
    except IntegrityError:
        return JSONResponse(status_code=400, content={"detail": "Такой email уже существует"})


# b. Просмотр строки из таблицы Users по id
@router.get("/users/{user_id}", response_model=UserSQL)
async def get_user(user_id: int = Path(...)):
    db: Session = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return JSONResponse(status_code=404, content={"detail": "Пользователь не найден"})
    return user


# c. Изменение строки в таблице Users по id
@router.put("/users/{user_id}", response_model=UserSQL)
async def update_user(user_id: int = Path(...), user: UserSQL = Body(...)):
    db: Session = next(get_db())
    user_to_update = db.query(User).filter(User.id == user_id).first()
    if not user_to_update:
        return JSONResponse(status_code=404, content={"detail": "Пользователь не найден"})
    user_to_update.name = user.name
    user_to_update.email = user.email
    db.commit()
    return user_to_update


# d. Удаление строки из таблицы Users по id
@router.delete("/users/{user_id}")
async def delete_user(user_id: int = Path(...)):
    db: Session = next(get_db())
    user_to_delete = db.query(User).filter(User.id == user_id).first()
    if not user_to_delete:
        return JSONResponse(status_code=404, content={"detail": "Пользователь не найден"})
    db.delete(user_to_delete)
    db.commit()
    return {"detail": "Пользователь удален"}
