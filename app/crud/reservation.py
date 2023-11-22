
from app.crud.base import CRUDBase
from app.models.reservation import Reservation


class CRUDReservation(CRUDBase):
    """CRUD-операции с бронированиями."""


reservation_crud = CRUDReservation(Reservation)
