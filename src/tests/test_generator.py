import os
import tempfile
from unittest import TestCase, mock
from zipfile import ZipFile

from entities import Document, DocumentObject
from generator import (
    generate_random_document, document_to_xml,
    # generate_zip_file_with_random_documents,
    generate_zip_files_with_random_documents,
)
from utils import filter_file_names, filter_file_paths


class GenerateRandomDocumentTestCase(TestCase):
    # TODO: Добавить тесты краевых условий
    def test_generate_random_document(self):
        mock_uuid4_value = '8e7838b8-be1e-47bb-9f4e-0ad3daca3bb9'
        excepted_document = Document(
            id_=mock_uuid4_value,
            level=5,  # Произвольное допустимое значение
            objects=[
                DocumentObject(name=mock_uuid4_value),
                DocumentObject(name=mock_uuid4_value),
            ]
        )
        with mock.patch('generator.uuid4', return_value=mock_uuid4_value):
            document = generate_random_document(
                min_level=excepted_document.level,
                max_level=excepted_document.level,
                min_objects_quantity=len(excepted_document.objects),
                max_objects_quantity=len(excepted_document.objects),
            )

            self.assertEqual(document, excepted_document)


class DocumentToXmlTestCase(TestCase):
    # TODO: Добавить тесты краевых условий
    def test_document_to_xml(self):
        document = Document(
            id_='8e7838b8-be1e-47bb-9f4e-0ad3daca3bb9',
            level=5,
            objects=[
                DocumentObject(name='49fj29nq-fj34-fk2p-9f4e-fj920v02fj29'),
                DocumentObject(name='l29j2ma4-vlq3-24jr-34ve-fvj349voa113'),
            ]
        )

        xml = document_to_xml(document)
        expected_xml = (
            f"<root>\n"
            f"    <var name='id' value='{document.id}'/>\n"
            f"    <var name='level' value='{document.level}'/>\n"
            f"    <objects>\n"
            f"        \n"
            f"            <object name='{document.objects[0].name}'/>\n"
            f"        \n"
            f"            <object name='{document.objects[1].name}'/>\n"
            f"        \n"
            f"    </objects>\n"
            f"</root>"
        )
        self.assertEqual(xml, expected_xml)


# TODO: Дописать тесты для `generate_zip_file_with_random_documents`


class GenerateZipFilesWithRandomDocumentsTestCase(TestCase):
    # TODO: Добавить тесты краевых условий
    def generate_zip_files_with_random_documents(self):
        with tempfile.TemporaryDirectory() as temp_dir_path:
            zip_files_quantity = 50
            documents_per_zip_file = 100
            verbose = False

            self.assertListEqual(os.listdir(temp_dir_path), [])
            generate_zip_files_with_random_documents(
                temp_dir_path, zip_files_quantity, documents_per_zip_file,
                verbose,
            )
            self.assertEqual(
                len(os.listdir(temp_dir_path)), zip_files_quantity,
            )
            self.assertListEqual(
                os.listdir(temp_dir_path),
                list(filter_file_names(temp_dir_path, 'zip')),
            )

            for zip_file_path in filter_file_paths(temp_dir_path, 'zip'):
                with ZipFile(zip_file_path, 'r') as zip_file:
                    self.assertEqual(
                        len(
                            [
                                file_name for file_name in zip_file.namelist()
                                if file_name.endswith('.xml')
                            ]
                        ),
                        documents_per_zip_file,
                    )

