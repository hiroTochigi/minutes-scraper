import shutil, tempfile
from os import path
from os import mkdir
from os import getcwd
import unittest

from download_minutes import get_pdf_directory_path
from download_minutes import get_downloaded_paths 

class TestGetPdfDirectoryPath(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_get_pdf_directory_path_with_directory(self):
        # Create a file in the temporary directory
        target_path = path.join(self.test_dir, 'pdf')
        mkdir(target_path)       
        self.assertEqual(get_pdf_directory_path(target_path), target_path)

    def test_get_pdf_directory_path_without_directory(self):
        # Create a file in the temporary directory
        target_path = path.join(self.test_dir, 'pdf')
        self.assertEqual(get_pdf_directory_path(target_path), target_path)

class TestGetDownloadedPaths(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_get_downloaded_paths_without_any_files(self):
        self.assertEqual(get_downloaded_paths(self.test_dir), [])

    def test_get_downloaded_paths_with_a_file(self):
        target_path = path.join(self.test_dir, "target.txt")
        with open(target_path, "w") as r:
            r.write("hello")
        self.assertEqual(get_downloaded_paths(self.test_dir), [target_path])

    def test_get_downloaded_paths_with_non_exist_file(self):
        target_path = path.join(self.test_dir, "target.txt")
        with open(target_path, "w") as r:
            r.write("hello")
        non_target_path = path.join(self.test_dir, "nontarget.txt")
        self.assertNotEqual(get_downloaded_paths(self.test_dir), [non_target_path])

if __name__ == '__main__':
    unittest.main()