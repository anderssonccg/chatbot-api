import io
import httpx
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from google import genai
from config.db import AsyncSessionLocal
from dependencies import get_resource_service
from models.user import User
from sqlmodel import select
from utils import auth

router = APIRouter()
client = genai.Client()

@router.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    await websocket.accept()

    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=4401)
        return

    try:
        user = await get_current_user_ws(token)

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

        documents = await get_documents()

        if documents:
            try:
                chat.send_message([
                    *documents,
                    "Estos son los documentos que debes tener en cuenta para todas las respuestas."
                ])
            except Exception as e:
                print("Error cargando documentos al chat:", e)

        await websocket.send_json({"status": "ready"})

    except Exception as e:
        print("Error preparando el chat:", e)
        await websocket.send_json({"error": "No se pudo inicializar el chat"})
        await websocket.close(code=1011)
        return

    try:
        while True:
            user_message = await websocket.receive_text()

            try:
                response = chat.send_message(user_message)
                await websocket.send_text(response.text)

            except Exception as e:
                print("Error procesando mensaje:", e)
                await websocket.send_json({"error": "Error procesando el mensaje, el modelo puede estar ocupado. Intente de nuevo mas tarde."})

    except WebSocketDisconnect:
        print("Cliente desconectado")

    except Exception as e:
        print(f"Error en WebSocket: {e}")
        await websocket.close(code=1011)


async def get_documents():
    async with AsyncSessionLocal() as session:
        service = get_resource_service(session)

        resources = await service.get_all_resources()

        uploaded_files = []

        for resource in resources:
            if resource.is_enabled:
                try:
                    resource_data = io.BytesIO(httpx.get(resource.url).content)
                    file_uploaded = client.files.upload(
                        file=resource_data,
                        config=dict(mime_type="application/pdf")
                    )
                    uploaded_files.append(file_uploaded)
                except Exception as e:
                    print(f"Error subiendo archivo {resource.url}: {e}")

    return uploaded_files


async def get_current_user_ws(token: str):
    async with AsyncSessionLocal() as session:
        user_id = auth.decode_token(token)

        if not user_id:
            raise Exception("Token inválido")

        result = await session.execute(
            select(User).where(User.id == int(user_id))
        )

        user = result.scalar_one_or_none()

        if not user:
            raise Exception("Usuario no encontrado")

        return user
