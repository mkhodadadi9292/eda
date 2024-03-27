from sqlmodel import SQLModel

class OrderingModel(SQLModel, table=False):
    user_id: int
    parking_slot_ref_no: str # uuid_product:uuid_ordering
    amount: int

