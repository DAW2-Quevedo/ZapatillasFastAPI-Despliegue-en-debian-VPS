from sqlmodel import SQLModel, create_engine, Session
from ..models.zapatilla import Zapatilla
from datetime import date
import os

# SQLite - simple y sin configuracion
DATABASE_PATH = os.getenv("DATABASE_PATH", "zapatillas.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        # Solo insertar datos si la tabla esta vacia
        existing = session.query(Zapatilla).first()
        if existing:
            return
        session.add(Zapatilla(id=1, marca="Nike", modelo="Air Max", talla=42.5, precio=120.0, tipo="Deportivo", color="Rojo", fecha_lanzamiento=date(2022, 1, 15)))
        session.add(Zapatilla(id=2, marca="Adidas", modelo="Ultraboost", talla=43.0, precio=150.0, tipo="Running", color="Negro", fecha_lanzamiento=date(2021, 11, 20)))
        session.add(Zapatilla(id=3, marca="Puma", modelo="Suede Classic", talla=41.0, precio=80.0, tipo="Casual", color="Blanco", fecha_lanzamiento=date(2020, 5, 10)))
        session.add(Zapatilla(id=4, marca="Reebok", modelo="Club C 85", talla=42.0, precio=90.0, tipo="Casual", color="Verde", fecha_lanzamiento=date(2019, 8, 25)))
        session.add(Zapatilla(id=5, marca="New Balance", modelo="574", talla=44.0, precio=100.0, tipo="Deportivo", color="Azul", fecha_lanzamiento=date(2021, 3, 30)))
        session.commit()
