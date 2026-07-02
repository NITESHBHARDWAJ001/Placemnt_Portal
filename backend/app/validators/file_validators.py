from flask import current_app

from app.utils.exceptions import ValidationError


def validate_resume_file(file_storage):
    if file_storage is None or file_storage.filename == "":
        raise ValidationError("No resume file provided")

    filename = file_storage.filename
    if "." not in filename or filename.rsplit(".", 1)[1].lower() not in current_app.config[
        "ALLOWED_RESUME_EXTENSIONS"
    ]:
        raise ValidationError("Only PDF files are allowed for resumes")

    file_storage.seek(0, 2)
    size = file_storage.tell()
    file_storage.seek(0)
    if size > current_app.config["MAX_CONTENT_LENGTH"]:
        raise ValidationError("Resume file exceeds the maximum allowed size (5MB)")
