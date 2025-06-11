from sqlalchemy import Column, String, Float, Boolean, Date
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class OfferORM(Base):
    __tablename__ = "offers"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    url = Column(String(255), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    price_per_meter = Column(Float, nullable=False)
    area = Column(Float, nullable=False)
    source = Column(String(100), nullable=False)
    found_date = Column(Date, nullable=False)
    favourite = Column(Boolean, default=False, nullable=False)
    hidden = Column(Boolean, default=False, nullable=False)
