import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename


def allowed_resume_file(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in current_app.config["ALLOWED_RESUME_EXTENSIONS"]


def save_resume_file(file_storage, student_id: int) -> tuple[str, str]:
    original_name = secure_filename(file_storage.filename)
    unique_name = f"{student_id}_{uuid.uuid4().hex}_{original_name}"
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)
    full_path = os.path.join(upload_folder, unique_name)
    file_storage.save(full_path)
    return original_name, full_path


def delete_file_if_exists(file_path: str) -> None:
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
