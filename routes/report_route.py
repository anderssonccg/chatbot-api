from fastapi import APIRouter, Depends
from dependencies import get_chat_service, get_current_user, get_message_service, get_user_service
from models.user import UserRead
from services.chat_service import ChatService
from services.message_service import MessageService
from services.user_service import UserService


router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/")
async def get_faq(
    user: UserRead = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
    message_service: MessageService = Depends(get_message_service),
    chat_service: ChatService = Depends(get_chat_service)
):
    users_count = await user_service.count_users()
    total_messages = await message_service.count_user_messages()
    daily_messages = await message_service.count_daily_user_messages()
    satisfaction_level_avg = await chat_service.get_average_satisfaction_level()
    average_response_time = await message_service.get_average_response_time()
    return {
        "total_users": users_count,
        "total_user_messages": total_messages,
        "daily_user_messages": daily_messages,
        "average_satisfaction_level": satisfaction_level_avg,
        "average_response_time": average_response_time
    }