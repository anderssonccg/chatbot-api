from typing import List, Optional
from fastapi import HTTPException, status
from models.chat import Chat, ChatCreate, ChatRead, ChatUpdate
from repositories.chat_repository import ChatRepository

class ChatService:

    def __init__(self, chat_repository: ChatRepository):
        self.chat_repository = chat_repository

    async def get_all_chats_by_user(self, user_id: int) -> List[ChatRead]:
        chats = await self.chat_repository.get_by_user(user_id)
        return [ChatRead.model_validate(chat) for chat in chats]
    
    async def get_all_chats(self) -> List[ChatRead]:
        chats = await self.chat_repository.get_all()
        return [ChatRead.model_validate(chat) for chat in chats]

    async def get_by_id(self, id: int) -> Optional[ChatRead]:
        chat = await self.chat_repository.get(id)
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chat inexistente."
            )
        return ChatRead.model_validate(chat)

    async def create(self, chat: ChatCreate) -> Chat:
        chat = Chat.model_validate(chat.dict())
        chat_created = await self.chat_repository.create(chat)
        return ChatRead.model_validate(chat_created)

    async def update(self, chat_id: int, chat_data: ChatUpdate) -> ChatRead:
        await self.get_by_id(chat_id)
        chat_data = chat_data.dict(exclude_unset=True)
        chat_updated = await self.chat_repository.update(chat_id, chat_data)
        return ChatRead.model_validate(chat_updated)

    async def delete(self, chat_id: int) -> bool:
        await self.get_by_id(chat_id)
        return await self.chat_repository.delete(chat_id)