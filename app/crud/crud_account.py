from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountUpdate


class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Account]:
        return db.query(self.model).filter(Account.name == name).first()


account = CRUDAccount(Account)
