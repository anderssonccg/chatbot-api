from typing import List, Optional
from sqlmodel import select
from sqlalchemy.orm import selectinload
from config.db import SessionDep
from models.chat import Chat
from repositories.repository_interface import IRepository

class ChatRepository(IRepository[Chat]):

    def __init__(self, session: SessionDep):
        self.session = session

    async def get_by_user(self, user_id: int) -> List[Chat]:
        result = await self.session.execute(
            select(Chat)
            .where(Chat.user_id == user_id)
            .options(selectinload(Chat.messages))
        )
        return result.scalars().all()

    async def get_all(self) -> List[Chat]:
        result = await self.session.execute(select(Chat))
        return result.scalars().all()

    async def get(self, id: int) -> Optional[Chat]:
        result = await self.session.execute(select(Chat).where(Chat.id == id))
        return result.scalars().first()

    async def create(self, chat: Chat) -> Chat:
        self.session.add(chat)
        await self.session.commit()
        await self.session.refresh(chat)
        return chat

    async def update(self, id: int, chat_data: Chat) -> Optional[Chat]:
        chat = await self.get(id)
        if chat:
            chat.sqlmodel_update(chat_data)
            await self.session.commit()
            await self.session.refresh(chat)
            return chat
        return None

    async def delete(self, id: int) -> bool:
        chat = await self.get(id)
        if chat:
            await self.session.delete(chat)
            await self.session.commit()
            return True
        return False