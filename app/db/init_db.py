from typing import Dict, Optional

from sqlalchemy.orm import Session

from app import crud, schemas
from app.constants.role import Role
from app.core.config import settings
from app.models.user import User


def init_db(db: Session) -> None:
    create_superadmin_account(db=db)
    superadmin_user = create_superadmin_user(db=db)
    create_default_role(db=db, default_role=Role.GUEST)
    create_default_role(db=db, default_role=Role.ACCOUNT_ADMIN)
    create_default_role(db=db, default_role=Role.ACCOUNT_MANAGER)
    create_default_role(db=db, default_role=Role.ADMIN)
    create_default_role(db=db, default_role=Role.SUPER_ADMIN)
    create_superadmin_user_role(db=db, superadmin_user=superadmin_user)


def create_superadmin_account(*, db: Session) -> None:
    account = crud.account.get_by_name(
        db, name=settings.FIRST_SUPER_ADMIN_ACCOUNT_NAME
    )
    if not account:
        account_in = schemas.AccountCreate(
            name=settings.FIRST_SUPER_ADMIN_ACCOUNT_NAME,
            description="superadmin account",
        )
        crud.account.create(db, obj_in=account_in)


def create_superadmin_user(*, db: Session) -> User:
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPER_ADMIN_EMAIL)
    if not user:
        account = crud.account.get_by_name(
            db, name=settings.FIRST_SUPER_ADMIN_ACCOUNT_NAME
        )
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPER_ADMIN_EMAIL,
            password=settings.FIRST_SUPER_ADMIN_PASSWORD,
            full_name=settings.FIRST_SUPER_ADMIN_EMAIL,
            account_id=account.id,
        )
        user = crud.user.create(db, obj_in=user_in)

    return user


def create_default_role(*, db: Session, default_role: Dict[str, str]) -> None:
    role = crud.role.get_by_name(db, name=default_role["name"])
    if not role:
        guest_role_in = schemas.RoleCreate(
            name=default_role["name"], description=default_role["description"]
        )
        crud.role.create(db, obj_in=guest_role_in)


def create_superadmin_user_role(
    *, db: Session, superadmin_user: Optional[User]
) -> None:
    user_role = crud.user_role.get_by_user_id(db, user_id=superadmin_user.id)
    if not user_role:
        role = crud.role.get_by_name(db, name=Role.SUPER_ADMIN["name"])
        user_role_in = schemas.UserRoleCreate(
            user_id=superadmin_user.id, role_id=role.id
        )
        crud.user_role.create(db, obj_in=user_role_in)
