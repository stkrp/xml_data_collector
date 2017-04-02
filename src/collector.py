"""
|================|===============|===================|======================|
| COLLECTOR TYPE | ZIPS QUANTITY | DOCUMENTS PER ZIP | DURATION (SEC)       |
|================|===============|===================|======================|
|  single core   |   50          |   100             |   0.95585036277771   |
|  multiple core |   50          |   100             |   0.8466031551361084 |
|----------------|---------------|-------------------|----------------------|
|  single core   |   500         |   1000            |   91.20046877861023  |
|  multiple core |   500         |   1000            |   54.7540442943573   |
|----------------|---------------|-------------------|----------------------|
|  single core   |   500         |   10000           |   938.2648339271545  |
|  multiple core |   500         |   10000           |   571.2564518451691  |
|----------------|---------------|-------------------|----------------------|
"""


import csv
import itertools
import multiprocessing
from io import TextIOWrapper
from typing import List, Iterable
from zipfile import ZipFile

from lxml import etree

from entities import Document, DocumentObject
from utils import filter_file_paths


def document_from_xml(xml: str) -> Document:
    xml_tree = etree.fromstring(xml)

    id_element = (xml_tree.xpath('(/root/var[@name="id"])[1]') or (None, ))[0]
    level_element = (
        (xml_tree.xpath('(/root/var[@name="level"])[1]') or (None, ))[0]
    )
    object_elements = xml_tree.xpath('/root/objects/object')

    return Document(
        id_=id_element.get('value') if id_element is not None else None,
        level=level_element.get('value') if level_element is not None else None,  # NoQA
        objects=[
            DocumentObject(name=object_element.get('name'))
            for object_element in object_elements
        ]
    )


def documents_from_zip_file(
    zip_file_path: str, verbose: bool = True,
) -> List[Document]:
    documents = []
    with ZipFile(zip_file_path, 'r') as zip_file:
        for zipped_file_name in zip_file.namelist():
            if not zipped_file_name.endswith('.xml'):
                continue

            with zip_file.open(zipped_file_name) as zipped_file:
                documents.append(
                    document_from_xml(zipped_file.read().decode('utf-8'))
                )

    if verbose:
        print(f'Documents from {zip_file_path} loaded')

    return documents


def documents_to_csv_files(
    documents: Iterable, documents_file: TextIOWrapper,
    objects_file: TextIOWrapper, write_headers: bool = True,
) -> None:
    # Используется однопоточная реализация
    # Для ускорения можно было бы попробовать разделить запись в два файла на
    # разные процессы (или потоки), чтобы каждый файл наполнялся отдельно,
    # но нужно измерить накладные расходы на общение между процессами
    # (переключение потоков)
    documents_writer = csv.writer(documents_file)
    objects_writer = csv.writer(objects_file)
    if write_headers:
        documents_writer.writerow(('id', 'level'))
        objects_writer.writerow(('id', 'name'))
    for document in documents:
        documents_writer.writerow((document.id, document.level))
        for object_ in document.objects:
            objects_writer.writerow((document.id, object_.name))


def collect_documents_info_single_core(
    dir_path: str, documents_file: TextIOWrapper, objects_file: TextIOWrapper,
    write_headers: bool = True,
) -> None:
    documents = itertools.chain.from_iterable(
        map(documents_from_zip_file, filter_file_paths(dir_path, 'zip'))
    )
    documents_to_csv_files(
        documents, documents_file, objects_file, write_headers,
    )


def collect_documents_info_multiple_core(
    dir_path: str, documents_file: TextIOWrapper, objects_file: TextIOWrapper,
    write_headers: bool = True,
) -> None:
    with multiprocessing.Pool() as pool:
        documents = itertools.chain.from_iterable(
            pool.imap_unordered(
                documents_from_zip_file, filter_file_paths(dir_path, 'zip'),
            )
        )
        documents_to_csv_files(
            documents, documents_file, objects_file, write_headers,
        )
        pool.close()
        pool.join()


if __name__ == '__main__':
    # https://docs.python.org/3/library/csv.html#id3
    with open('docs.csv', 'wt', encoding='utf-8', newline='') as docs_fh, \
         open('objs.csv', 'wt', encoding='utf-8', newline='') as objs_fh:

        collect_documents_info_multiple_core('documents', docs_fh, objs_fh)
