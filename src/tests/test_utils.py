import os
import tempfile
from unittest import TestCase
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
