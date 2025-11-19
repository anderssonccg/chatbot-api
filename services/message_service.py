from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException, status
from models.message import Message, MessageCreate, MessageRead, MessageUpdate
from repositories.message_repository import MessageRepository

class MessageService:

    def __init__(self, message_repository: MessageRepository):
        self.message_repository = message_repository

    async def count_user_messages(self) -> int:
        return await self.message_repository.count_user_messages()
    
    async def count_daily_user_messages(self) -> int:
        date = datetime.utcnow()
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        return await self.message_repository.count_daily_user_messages(date=start_of_day)
    
    async def get_average_response_time(self) -> float:
        return await self.message_repository.get_average_response_time()

    async def get_all_messages_by_chat(self, chat_id: int) -> List[MessageRead]:
        messages = await self.message_repository.get_by_chat(chat_id)
        return [MessageRead.model_validate(message) for message in messages]
    
    async def get_all_messages(self) -> List[MessageRead]:
        messages = await self.message_repository.get_all()
        return [MessageRead.model_validate(message) for message in messages]

    async def get_by_id(self, id: int) -> Optional[MessageRead]:
        message = await self.message_repository.get(id)
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Mensaje inexistente."
            )
        return MessageRead.model_validate(message)

    async def create(self, message: MessageCreate) -> MessageRead:
        message = Message.model_validate(message.dict())
        message_created = await self.message_repository.create(message)
        return MessageRead.model_validate(message_created)

    async def update(self, message_id: int, message_data: MessageUpdate) -> MessageRead:
        await self.get_by_id(message_id)
        message_data = message_data.dict(exclude_unset=True)
        message_updated = await self.message_repository.update(message_id, message_data)
        return MessageRead.model_validate(message_updated)

    async def delete(self, message_id: int) -> bool:
        await self.get_by_id(message_id)
        return await self.message_repository.delete(message_id)