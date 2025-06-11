# infrastructure/db/repositories.py
from sqlalchemy.orm import Session
from app.models.domain import Offer
from app.models.entities import OfferORM
from uuid import UUID
from typing import List
from dataclasses import asdict


class OfferRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, offer_id: UUID) -> Offer | None:
        orm = self._session.get(OfferORM, offer_id)
        return self._to_domain(orm) if orm else None

    def list(self) -> List[Offer]:
        return [self._to_domain(o) for o in self._session.query(OfferORM).all()]

    def save(self, offer: Offer) -> None:
        self._session.merge(self._to_orm(offer))
        self._session.commit()

    def save_all(self, offers: List[Offer]) -> None:
        orm_objects = [self._to_orm(o) for o in offers]
        self._session.bulk_save_objects(orm_objects)
        self._session.commit()

    def delete(self, offer_id: UUID) -> None:
        self._session.query(OfferORM).filter_by(id=offer_id).delete()
        self._session.commit()

    def exists_by_url(self, url: str) -> bool:
        return self._session.query(OfferORM).filter_by(url=url).first() is not None

    def _to_domain(self, orm: OfferORM) -> Offer:
        return Offer( 
            id=orm.id,
            url=orm.url,
            title=orm.title,
            price=orm.price,
            price_pet_meter=orm.price_per_meter,
            area=orm.area,
            source=orm.source,
            found_date=orm.found_date,
            favourite=orm.favourite,
            hidden=orm.hidden
        )

    def _to_orm(self, offer: Offer) -> OfferORM:
        return OfferORM(**asdict(offer))
