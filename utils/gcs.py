import os, ast
from fastapi import HTTPException, UploadFile
from google.cloud import storage
from google.oauth2 import service_account

credentials_json = os.getenv("GOOGLE_CREDENTIALS")
credentials_dict = ast.literal_eval(credentials_json)
credentials_dict["private_key"] = credentials_dict["private_key"].replace("\\n", "\n")
credentials = service_account.Credentials.from_service_account_info(credentials_dict)
storage_client = storage.Client(credentials=credentials, project=credentials.project_id)

BUCKET_NAME = os.getenv("BUCKET_NAME")


def generate_unique_filename(bucket, filename):
    base_name, ext = os.path.splitext(filename)
    index = 1
    new_filename = filename

    while bucket.blob(new_filename).exists():
        new_filename = f"{base_name}({index}){ext}"
        index += 1

    return new_filename


def upload_file(file: UploadFile):
    bucket = storage_client.bucket(BUCKET_NAME)
    unique_name = generate_unique_filename(bucket, file.filename)
    blob = bucket.blob(unique_name)
    blob.upload_from_file(file.file, content_type=file.content_type)
    return {
        "url": f"https://storage.googleapis.com/{BUCKET_NAME}/{unique_name}",
        "filename": unique_name,
    }


def delete_file(filename: str):
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    if blob.exists():
        blob.delete()
        return
    else:
        raise HTTPException(status_code=404, detail="El archivo no existe.")
