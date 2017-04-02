import os
import tempfile
from unittest import TestCase, mock

from entities import Document, DocumentObject
from generator import (
    generate_random_document, document_to_xml,
    # generate_zip_file_with_random_documents,
    # generate_zip_files_with_random_documents,
)
from utils import clear_directory, filter_file_names


class OsShortcutsTestCaseMixin:
    def create_empty_file(self, dir_path: str, file_name: str) -> str:
        file_path = os.path.join(dir_path, file_name)
        open(file_path, 'wb').close()
        self.assertTrue(os.path.exists(file_path))
        return file_path


class ClearDirectoryTestCase(OsShortcutsTestCaseMixin, TestCase):
    def test_clear_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir_path:
            non_empty_dir_path = os.path.join(
                temp_dir_path, 'non_empty_directory',
            )

            os.makedirs(non_empty_dir_path)
            self.assertTrue(os.path.exists(non_empty_dir_path))
            self.create_empty_file(non_empty_dir_path, 'some_file_1')
            self.create_empty_file(non_empty_dir_path, 'some_file_2')
            os.makedirs(os.path.join(non_empty_dir_path, 'some_directory'))
            self.assertTrue(os.listdir(non_empty_dir_path))

            clear_directory(non_empty_dir_path)

            self.assertTrue(os.path.exists(non_empty_dir_path))
            self.assertFalse(os.listdir(non_empty_dir_path))

        self.assertFalse(os.path.exists(temp_dir_path))

    def test_clear_empty_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir_path:
            empty_dir_path = os.path.join(temp_dir_path, 'empty_directory')

            os.makedirs(empty_dir_path)
            self.assertTrue(os.path.exists(empty_dir_path))
            self.assertFalse(os.listdir(empty_dir_path))

            clear_directory(empty_dir_path)

            self.assertTrue(os.path.exists(empty_dir_path))
            self.assertFalse(os.listdir(empty_dir_path))

        self.assertFalse(os.path.exists(temp_dir_path))

    def test_clear_non_existent_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir_path:
            non_existent_dir_path = os.path.join(
                temp_dir_path, 'non_existent_directory',
            )

            self.assertFalse(os.path.exists(non_existent_dir_path))
            clear_directory(non_existent_dir_path)
            self.assertFalse(os.path.exists(non_existent_dir_path))

        self.assertFalse(os.path.exists(temp_dir_path))


class FilterFileNamesTestCase(OsShortcutsTestCaseMixin, TestCase):
    def test_filter_files(self):
        with tempfile.TemporaryDirectory() as temp_dir_path:
            zip_file_name = 'temp.zip'
            txt_file_name = 'temp.txt'
            untyped_file_name = 'temp'
            for file_name in (zip_file_name, txt_file_name, untyped_file_name):
                self.create_empty_file(temp_dir_path, file_name)

            os.makedirs(os.path.join(temp_dir_path, 'some_directory'))

            self.assertSetEqual(
                set(filter_file_names(temp_dir_path)),
                {zip_file_name, txt_file_name, untyped_file_name}
            )

        self.assertFalse(os.path.exists(temp_dir_path))

    def test_filter_zip_files(self):
        with tempfile.TemporaryDirectory() as temp_dir_path:
            zip_file_name = 'temp.zip'
            txt_file_name = 'temp.txt'
            untyped_file_name = 'temp'
            for file_name in (zip_file_name, txt_file_name, untyped_file_name):
                self.create_empty_file(temp_dir_path, file_name)

            os.makedirs(os.path.join(temp_dir_path, 'some_directory'))

            self.assertSetEqual(
                set(filter_file_names(temp_dir_path, 'zip')),
                {zip_file_name}
            )

        self.assertFalse(os.path.exists(temp_dir_path))

    def test_filter_files_in_empty_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir_path:
            self.assertFalse(os.listdir(temp_dir_path))
            self.assertSetEqual(set(filter_file_names(temp_dir_path)), set())

        self.assertFalse(os.path.exists(temp_dir_path))


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

            self.assertEquals(document, excepted_document)


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
        self.assertEquals(xml, expected_xml)


# TODO: Дописать тесты для `generate_zip_file_with_random_documents`
# TODO: Дописать тесты для `generate_zip_files_with_random_documents`
