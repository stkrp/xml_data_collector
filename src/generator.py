import os
from functools import partial
from multiprocessing import Pool
from random import randint
from uuid import uuid4
from zipfile import ZipFile

from jinja2 import Environment, PackageLoader

from entities import Document, DocumentObject
from utils import clear_directory


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
)-> Document:
    return Document(
        id_=str(uuid4()),
        level=randint(min_level, max_level),
        objects=[
            DocumentObject(name=str(uuid4()))
            for _ in range(randint(min_objects_quantity, max_objects_quantity))
        ],
    )


def document_to_xml(
    document: Document, template_name: str = DEFAULT_XML_TEMPLATE_NAME,
    template_env: Environment = DEFAULT_TEMPLATE_ENV,
) -> str:
    return template_env.get_template(template_name).render(document=document)


def generate_zip_file_with_random_documents(
    zip_file_path: str, documents_per_file: int, verbose: bool = True
) -> None:
    with ZipFile(zip_file_path, 'w') as zip_file:
        for document_num in range(documents_per_file):
            zip_file.writestr(
                f'{document_num}.xml',
                document_to_xml(generate_random_document()),
            )

    if verbose:
        print(f'{zip_file_path} created')


def generate_zip_files_with_random_documents(
    dir_path: str, quantity: int, documents_per_file: int,
    verbose: bool = True,
) -> None:
    if os.path.exists(dir_path):
        clear_directory(dir_path)
    else:
        os.makedirs(dir_path)

    zip_file_paths = (
        os.path.join(dir_path, f'{zip_file_num}.zip')
        for zip_file_num in range(quantity)
    )

    generate_zip_file = partial(
        generate_zip_file_with_random_documents,
        documents_per_file=documents_per_file, verbose=verbose,
    )

    with Pool() as pool:
        # TODO: Добавить расчет `chunksize`
        pool.imap_unordered(generate_zip_file, zip_file_paths)
        pool.close()
        pool.join()


if __name__ == '__main__':
    generate_zip_files_with_random_documents('documents', 500, 1000)
