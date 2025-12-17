from sqlmodel import SQLModel, create_engine,Session
from models.zapatilla import Zapatilla

db_user: str = "root"
db_password: str = "password"
db_host: str = "localhost"
db_port: str = "3306"
db_name: str = "zapatillasdb"

DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Zapatilla(id=1,marca="Nike", modelo="Air Max", talla=42.5, precio=120.0, tipo="Deportivo", color="Rojo", fecha_lanzamiento="2022-01-15"))
        session.add(Zapatilla(id=2,marca="Adidas", modelo="Ultraboost", talla=43.0, precio=150.0, tipo="Running", color="Negro", fecha_lanzamiento="2021-11-20"))
        session.add(Zapatilla(id=3,marca="Puma", modelo="Suede Classic", talla=41.0, precio=80.0, tipo="Casual", color="Blanco", fecha_lanzamiento="2020-05-10"))
        session.add(Zapatilla(id=4,marca="Reebok", modelo="Club C 85", talla=42.0, precio=90.0, tipo="Casual", color="Verde", fecha_lanzamiento="2019-08-25"))
        session.add(Zapatilla(id=5,marca="New Balance", modelo="574", talla=44.0, precio=100.0, tipo="Deportivo", color="Azul", fecha_lanzamiento="2021-03-30"))
        session.commit()
        
