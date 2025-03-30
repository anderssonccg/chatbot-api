# Chatbot Asesor Academico API

## Tecnologias utilizadas

- FastAPI [Documentacion](https://fastapi.tiangolo.com/)
- SQLModel: ORM para base de datos. [Documentacion](https://sqlmodel.tiangolo.com/)
- PostgreSQL: Base de datos
- JWT: Autenticacion
- Google Cloud Storage: Almacenamiento de archivos

## Comenzar
1. Clonar el repositorio
```bash
git clone repo
```
2. Crear y activar entorno virtual
```bash
python -m venv venv
source ./venv/bin/activate # Linux
.\venv\Scripts\activate # Windows
```
3. Instalar dependencias
```bash
pip install -r requirements.txt
```
4. Crear un archivo .env en la raiz del proyecto y declarar las variables de entorno
5. Correr el servidor en modo desarrollo
```bash
fastapi dev main.py
```