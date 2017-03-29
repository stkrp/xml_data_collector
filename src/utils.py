import os
import shutil
from typing import Generator


def filter_file_names(
    dir_path: str, extension: str = None,
) -> Generator[str, None, None]:
    file_names = (
        name for name in os.listdir(dir_path)
        if os.path.isfile(os.path.join(dir_path, name))
    )
    if extension:
        extension_with_dot = f'.{extension}'
        file_names = (
            name for name in file_names if name.endswith(extension_with_dot)
        )

    return file_names


def clear_directory(dir_path: str) -> None:
    """ 
    Удаляет папку и создает заново

    НЕЛЬЗЯ использовать, если важны параметры оригинальной папки, например, 
    права, или, если недостаточно прав для создания папки.
    """
    # Проверяем, что папка существует, чтобы не создать при удалении папку,
    # которой до удаления не было
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path, ignore_errors=True)
        os.makedirs(dir_path, exist_ok=True)
