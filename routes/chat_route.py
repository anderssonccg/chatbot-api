import io
from typing import List
import httpx
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from google import genai
from config.db import AsyncSessionLocal
from dependencies import get_chat_service, get_current_user, get_message_service, get_resource_service
from models.message import MessageCreate
from models.user import User
from sqlmodel import select
from utils import auth
from models.chat import ChatCreate, ChatRead
from datetime import datetime

router = APIRouter()
client = genai.Client()

@router.get("/chats", response_model=List[ChatRead])
async def get_chats(
    user: User = Depends(get_current_user),
    service = Depends(get_chat_service),
):
    return await service.get_all_chats_by_user(user.id)


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

        chat_id = await create_chat_in_db(user.id)
        await websocket.send_json({
            "chat_id": chat_id,
            "status": "ready"
        })

    except Exception as e:
        print("Error preparando el chat:", e)
        await websocket.send_json({"error": "No se pudo inicializar el chat"})
        await websocket.close(code=1011)
        return

    try:
        while True:
            user_message = await websocket.receive_text()
            await save_message_in_db(chat_id, user_message, role="user")
            try:
                response = chat.send_message(user_message)
                await save_message_in_db(chat_id, response.text, role="chatbot")
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


async def create_chat_in_db(user_id: int):
    async with AsyncSessionLocal() as session:
        try:
            chat_service = get_chat_service(session)
            chat_created = await chat_service.create(
                ChatCreate(
                    user_id=user_id,
                    titulo="Chat iniciado el " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )
            )
            return chat_created.id
        except Exception as e:
            print(f"Error creando chat en BD: {e}")
            await session.rollback()
            raise

async def save_message_in_db(chat_id: int, texto: str, role: str):
    async with AsyncSessionLocal() as session:
        try:
            message = MessageCreate(
                chat_id=chat_id,
                texto=texto,
                role=role
            )
            message_service = get_message_service(session)
            await message_service.create(message)
        except Exception as e:
            print(f"Error guardando mensaje en BD: {e}")
            await session.rollback()
            raise