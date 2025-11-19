from datetime import datetime
from typing import List, Optional
from sqlmodel import func, select
from config.db import SessionDep
from models.message import Message
from repositories.repository_interface import IRepository

class MessageRepository(IRepository[Message]):

    def __init__(self, session: SessionDep):
        self.session = session

    async def count_user_messages(self) -> int:
        query = select(func.count()).select_from(Message).where(Message.role == 'user')
        result = await self.session.execute(query)
        return result.scalar_one()

    async def count_daily_user_messages(self, date: datetime) -> int:
        query = select(func.count()).select_from(Message).where(
            Message.role == 'user',
            Message.fecha >= date
        )
        result = await self.session.execute(query)
        return result.scalar_one()
    
    async def get_average_response_time(self) -> float:
        query = select(func.avg(Message.response_time)).where(Message.role == 'chatbot')
        result = await self.session.execute(query)
        average = result.scalar_one()
        return average if average is not None else 0.0

    async def get_by_chat(self, chat_id: int) -> List[Message]:
        result = await self.session.execute(select(Message).where(Message.chat_id == chat_id))
        return result.scalars().all()

    async def get_all(self) -> List[Message]:
        result = await self.session.execute(select(Message))
        return result.scalars().all()

    async def get(self, id: int) -> Optional[Message]:
        result = await self.session.execute(select(Message).where(Message.id == id))
        return result.scalars().first()

    async def create(self, message: Message) -> Message:
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def update(self, id: int, message_data: Message) -> Optional[Message]:
        message = await self.get(id)
        if message:
            message.sqlmodel_update(message_data)
            await self.session.commit()
            await self.session.refresh(message)
            return message
        return None

    async def delete(self, id: int) -> bool:
        message = await self.get(id)
        if message:
            await self.session.delete(message)
            await self.session.commit()
            return True
        return False