from app.models.domain_model import User
from app.schemas.user import UserCreate
from app.services import user_uow


def create_user(create_obj: UserCreate, uow: user_uow.AbstractUnitOfWork):
    with uow:
       db_obj = User(**create_obj.dict()) 
        
