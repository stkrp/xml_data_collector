import os
import tempfile
from unittest import TestCase
from zipfile import ZipFile

from generator import document_to_xml, generate_random_document
from collector import (
    collect_documents_info_single_core, collect_documents_info_multiple_core,
)


class CollectDocumentsInfoTestCaseMixin(object):
    # TODO: Добавить тесты краевых условий
    collector_callable = NotImplemented

    @property
    def collector(self):
        return self.__class__.collector_callable

    def test_collect_documents_info(self):
        document_1_1 = generate_random_document()
        document_1_2 = generate_random_document()
        zip_1 = (document_1_1, document_1_2)

        document_2_1 = generate_random_document()
        document_2_2 = generate_random_document()
        zip_2 = (document_2_1, document_2_2)

        with tempfile.TemporaryDirectory() as temp_dir_path:
            self.assertListEqual(os.listdir(temp_dir_path), [])

            documents_dir_path = os.path.join(temp_dir_path, 'documents')
            os.makedirs(documents_dir_path)

            for zip_num, zip_documents in enumerate((zip_1, zip_2)):
                zip_file_path = os.path.join(
                    documents_dir_path, f'{zip_num}.zip'
                )
                with ZipFile(zip_file_path, 'w') as zip_file:
                    for document_num, document in enumerate(zip_documents):
                        zip_file.writestr(
                            f'{document_num}.xml',
                            document_to_xml(document),
                        )

            self.assertListEqual(
                os.listdir(documents_dir_path), ['0.zip', '1.zip'],
            )
            documents_info_file_path = os.path.join(
                temp_dir_path, 'documents.csv',
            )
            objects_info_file_path = os.path.join(temp_dir_path, 'objects.csv')

            with open(
                     documents_info_file_path, 'wt', encoding='utf-8',
                     newline='',
                 ) as docs_fh, \
                 open(
                     objects_info_file_path, 'wt', encoding='utf-8',
                     newline='',
                 ) as objs_fh:

                self.collector(documents_dir_path, docs_fh, objs_fh)

            with open(
                     documents_info_file_path, 'rt', encoding='utf-8'
                 ) as docs_fh, \
                 open(
                     objects_info_file_path, 'rt', encoding='utf-8',
                 ) as objs_fh:

                expected_documents_info = {
                    f'{document.id},{document.level}'
                    for document in zip_1 + zip_2
                }
                self.assertSetEqual(
                    set(map(str.strip, docs_fh)),
                    expected_documents_info | {'id,level'},
                )

                expected_objects_info = {
                    f'{document.id},{object_.name}'
                    for document in zip_1 + zip_2
                    for object_ in document.objects
                }
                self.assertSetEqual(
                    set(map(str.strip, objs_fh)),
                    expected_objects_info | {'id,name'},
                )


class CollectDocumentsInfoSingleCoreTestCase(
    CollectDocumentsInfoTestCaseMixin, TestCase,
):
    collector_callable = collect_documents_info_single_core


class CollectDocumentsInfoMultipleCoreTestCase(
    CollectDocumentsInfoTestCaseMixin, TestCase,
):
    collector_callable = collect_documents_info_multiple_core
