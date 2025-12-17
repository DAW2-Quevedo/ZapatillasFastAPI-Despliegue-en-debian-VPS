from sqlmodel import Session, select
from models.zapatilla import Zapatilla

class SeriesRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def get_all_zapatillas(self) -> list[Zapatilla]:
        zapatillas = self.session.exec(select(Zapatilla)).all()
        return zapatillas   

    def get_zapatilla(self, zapatilla_id: int) -> Zapatilla:
        zapatilla = self.session.get(Zapatilla, zapatilla_id)
        return zapatilla
    def create_zapatilla(self, zapatilla: Zapatilla) -> Zapatilla:
        self.session.add(zapatilla)
        self.session.commit()
        self.session.refresh(zapatilla)
        return zapatilla
    
    def update_zapatilla(self, zapatilla_id: int, zapatilla_data: dict) -> Zapatilla:
        zapatilla = self.get_zapatilla(zapatilla_id)
        for key, value in zapatilla_data.items():
            setattr(zapatilla, key, value)
        self.session.commit()
        self.session.refresh(zapatilla)
        return zapatilla

    def delete_zapatilla(self, zapatilla_id: int) -> None:
        zapatilla = self.get_zapatilla(zapatilla_id)
        self.session.delete(zapatilla)
        self.session.commit()