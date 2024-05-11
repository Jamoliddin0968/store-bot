from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import ImageType as _FileType


class ImageType(_FileType):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(storage=FileSystemStorage(path='/tmp'), *args, **kwargs)
