import os
import tempfile
import unittest
from unittest.mock import patch

from src.database import add_student, delete_student, get_student, load_students, normalize_roll
from src.capture_faces import finalize_capture


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.students_file = os.path.join(self.temp_dir.name, "students.json")
        self.dataset_dir = os.path.join(self.temp_dir.name, "dataset")
        self.students_patch = patch("src.database.STUDENTS_JSON", self.students_file)
        self.dataset_patch = patch("src.database.DATASET_DIR", self.dataset_dir)
        self.students_patch.start()
        self.dataset_patch.start()
        self.addCleanup(self.temp_dir.cleanup)
        self.addCleanup(self.students_patch.stop)
        self.addCleanup(self.dataset_patch.stop)

    def test_normalize_roll_canonicalizes_positive_numbers(self):
        self.assertEqual(normalize_roll(" 00101 "), "101")

    def test_normalize_roll_rejects_non_numeric_and_zero_values(self):
        for roll in ("", "abc", "0", "-1"):
            with self.subTest(roll=roll):
                with self.assertRaises(ValueError):
                    normalize_roll(roll)

    def test_add_and_get_student_use_canonical_roll(self):
        add_student("00101", "  Ada Student  ", "Female")

        self.assertEqual(
            get_student("101"),
            {"name": "Ada Student", "gender": "Female"},
        )

    def test_corrupt_student_file_is_reported(self):
        with open(self.students_file, "w", encoding="utf-8") as file:
            file.write("{")

        with self.assertRaisesRegex(RuntimeError, "Could not read student database"):
            load_students()

    def test_delete_removes_student_and_matching_samples(self):
        add_student("101", "Ada Student", "Female")
        os.makedirs(os.path.join(self.dataset_dir, "101_Ada_Student"))
        os.makedirs(os.path.join(self.dataset_dir, "1010_Other"))

        self.assertTrue(delete_student("101"))
        self.assertIsNone(get_student("101"))
        self.assertFalse(os.path.exists(os.path.join(self.dataset_dir, "101_Ada_Student")))
        self.assertTrue(os.path.isdir(os.path.join(self.dataset_dir, "1010_Other")))

    def test_empty_capture_does_not_register_student(self):
        with patch("src.capture_faces.add_student") as add_student_mock:
            with self.assertRaisesRegex(ValueError, "No face samples were captured"):
                finalize_capture("101", "Ada Student", "Female", 0)

        add_student_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
