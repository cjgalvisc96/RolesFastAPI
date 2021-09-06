from sqlalchemy.orm import Session

from app import crud
from app.models.role import Role
from app.schemas.role import RoleCreate


def test_get_roles(db: Session) -> None:
    role_in_1 = RoleCreate(name="customer", description="customer")
    role_in_2 = RoleCreate(name="new role", description="new role")

    role_1 = crud.role.create(db, obj_in=role_in_1)
    role_2 = crud.role.create(db, obj_in=role_in_2)

    roles = crud.role.get_multi(db)

    assert role_1
    assert role_2
    assert type(role_1) is Role
    assert type(role_2) is Role
    assert len(roles) > 1
