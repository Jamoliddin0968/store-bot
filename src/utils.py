import os
import uuid
from typing import BinaryIO

from fastapi import UploadFile

from src.repositories import WordsRepo

word_repo = WordsRepo()


def get_word(value: str, language: str) -> str:
    word = word_repo.get_by_word(value)
    language = language.value
    if not word:
        return value
    if language == "uz" and word.value_uz:
        return word.value_uz
    if language == "ru" and word.value_ru:
        return word.value_ru
    if language == "en" and word.value_en:
        return word.value_en
    return value


def _get_file_extension(filename):
    extension = filename.split('.')[-1].lower()
    return "jpg"


def _generate_uuid():
    return str(uuid.uuid4())


def save_image(file, folder="") -> str:
    print(file)
    file_name = f"{_generate_uuid()}.{_get_file_extension(file.filename)}"
    directory = os.path.join("uploads", folder)
    file_path = os.path.join(directory, file_name)
    os.makedirs(directory, exist_ok=True)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    file_path = file_path.replace("\\", "/")
    return file_path
