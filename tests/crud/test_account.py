from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, schemas
from app.models.account import Account
from tests.utils.utils import random_lower_string


def test_create_account(db: Session) -> None:
    account_name = random_lower_string()
    account_description = random_lower_string()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = crud.account.create(db, obj_in=account_in)
    assert type(account) is Account
    assert hasattr(account, "name")
    assert hasattr(account, "description")
    assert account.name == account_name
    assert account.description == account_description
    assert account.is_active


def test_get_account(db: Session) -> None:
    account_name = random_lower_string()
    account_description = random_lower_string()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = crud.account.create(db, obj_in=account_in)
    account_2 = crud.account.get(db, id=account.id)
    assert account_2
    assert type(account) is Account
    assert jsonable_encoder(account) == jsonable_encoder(account_2)


def test_get_account_by_name(db: Session) -> None:
    account_name = random_lower_string()
    account_description = random_lower_string()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = crud.account.create(db, obj_in=account_in)
    account_2 = crud.account.get_by_name(db, name=account_name)
    assert account_2
    assert type(account) is Account
    assert jsonable_encoder(account) == jsonable_encoder(account_2)


def test_update_account(db: Session) -> None:
    account_name = random_lower_string()
    account_description = random_lower_string()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = crud.account.create(db, obj_in=account_in)
    new_account_name = random_lower_string()
    account_in_update = schemas.AccountUpdate(name=new_account_name)
    crud.account.update(db, db_obj=account, obj_in=account_in_update)
    account_2 = crud.account.get(db, id=account.id)
    assert account_2
    assert type(account) is Account
    assert account.description == account_2.description
    assert account_2.name == new_account_name
