import os
import shutil
from random import randint
from uuid import uuid4
from zipfile import ZipFile

from jinja2 import Environment, PackageLoader


# Documents generator
DEFAULT_MIN_LEVEL = 1
DEFAULT_MAX_LEVEL = 100
DEFAULT_MIN_OBJECTS_QUANTITY = 1
DEFAULT_MAX_OBJECTS_QUANTITY = 10

# Templates
DEFAULT_TEMPLATE_ENV = Environment(loader=PackageLoader('generator'))
DEFAULT_XML_TEMPLATE_NAME = 'document.xml'


def generate_random_document(
    min_level: int = DEFAULT_MIN_LEVEL,
    max_level: int = DEFAULT_MAX_LEVEL,
    min_objects_quantity: int = DEFAULT_MIN_OBJECTS_QUANTITY,
    max_objects_quantity: int = DEFAULT_MAX_OBJECTS_QUANTITY,
)-> dict:
    return {
        'id': str(uuid4()),
        'level': randint(min_level, max_level),
        'objects': [
            {'name': str(uuid4())}
            for _ in range(randint(min_objects_quantity, max_objects_quantity))
        ]
    }


def document_to_xml(
    document: dict, template_name: str = DEFAULT_XML_TEMPLATE_NAME,
    template_env: Environment = DEFAULT_TEMPLATE_ENV,
) -> str:
    return template_env.get_template(template_name).render(document)


def generate_zip_files_with_random_documents(
    quantity: int, documents_per_file: int, dir_path: str,
    verbose: bool = True,
) -> None:
    _clear_directory(dir_path)

    for zip_file_num in range(quantity):
        zip_file_path = os.path.join(dir_path, f'{zip_file_num}.zip')
        with ZipFile(zip_file_path, 'w') as zip_file:
            for document_num in range(documents_per_file):
                zip_file.writestr(
                    f'{document_num}.xml',
                    document_to_xml(generate_random_document()),
                )

        if verbose:
            print(f'{zip_file_path} created')


def _clear_directory(path: str) -> None:
    """ 
    Удаляет папку и создает заново

    НЕЛЬЗЯ использовать, если важны параметры оригинальной папки, например, 
    права, или если недостаточно прав для создания папки.
    """
    shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path, exist_ok=True)


if __name__ == '__main__':
    generate_zip_files_with_random_documents(50, 100, 'documents')
