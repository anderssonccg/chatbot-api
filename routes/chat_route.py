from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from google import genai
from dependencies import get_current_user
from models.user import UserRead

router = APIRouter()

@router.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    await websocket.accept()

    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=4401)
        return

    user: UserRead = await get_current_user(token)
    if not user:
        await websocket.close(code=4401)
        return

    client = genai.Client()
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config={
            "system_instruction": (
                "Eres un asistente académico de Ingeniería de Sistemas de la "
                "Universidad Francisco de Paula Santander. "
                "Responde de manera clara, amable y precisa."
            )
        }
    )

    try:
        while True:
            user_message = await websocket.receive_text()

            response_stream = chat.send_message_stream(user_message)

            for chunk in response_stream:
                if chunk.text:
                    await websocket.send_text(chunk.text)

            await websocket.send_json({"status": "fin del mensaje"})

    except WebSocketDisconnect:
        print("Cliente desconectado")

    except Exception as e:
        print(f"Error en WebSocket: {e}")
        await websocket.close(code=1011)
