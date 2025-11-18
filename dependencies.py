from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from config.db import SessionDep
from models.user import UserRead
from repositories.category_repository import CategoryRepository
from repositories.faq_repository import FAQRepository
from repositories.resource_repository import ResourceRepository
from repositories.user_repository import UserRepository
from services.category_service import CategoryService
from services.faq_service import FAQService
from services.resource_service import ResourceService
from services.user_service import UserService
from repositories.chat_repository import ChatRepository
from services.chat_service import ChatService
from services.message_service import MessageService
from repositories.message_repository import MessageRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_user_service(session: SessionDep) -> UserService:
    user_repository = UserRepository(session)
    return UserService(user_repository)


def get_resource_service(session: SessionDep) -> ResourceService:
    resource_repository = ResourceRepository(session)
    return ResourceService(resource_repository)


def get_category_service(session: SessionDep) -> CategoryService:
    category_repository = CategoryRepository(session)
    return CategoryService(category_repository)


def get_faq_service(session: SessionDep) -> FAQService:
    faq_repository = FAQRepository(session)
    return FAQService(faq_repository)

def get_chat_service(session: SessionDep) -> ChatService:
    chat_repository = ChatRepository(session)
    return ChatService(chat_repository)

def get_message_service(session: SessionDep) -> MessageService:
    message_repository = MessageRepository(session)
    return MessageService(message_repository)


def check_role(required_role: str):
    async def role_checker(user: UserRead = Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No estas autorizado para realizar esta accion.",
            )
        return user

    return role_checker


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service),
) -> UserRead:
    return await service.get_current_user(token)
