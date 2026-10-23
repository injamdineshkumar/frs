import json
import os
import shutil
from config import STUDENTS_JSON, DATASET_DIR


def normalize_roll(roll) -> str:
    """Return a canonical positive numeric roll number."""
    value = str(roll).strip()
    if not value.isdecimal() or int(value) <= 0:
        raise ValueError("Roll number must be a positive number.")
    return str(int(value))


def load_students() -> dict:
    """Load the student records dictionary from JSON file."""
    if not os.path.exists(STUDENTS_JSON):
        return {}
    try:
        with open(STUDENTS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Could not read student database at {STUDENTS_JSON}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"Student database at {STUDENTS_JSON} must contain a JSON object.")
    return data


def save_students(data: dict):
    """Save the student records dictionary to JSON file."""
    os.makedirs(os.path.dirname(STUDENTS_JSON), exist_ok=True)
    with open(STUDENTS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def add_student(roll, name, gender):
    """Add or update a student record."""
    roll = normalize_roll(roll)
    if not str(name).strip():
        raise ValueError("Student name cannot be empty.")
    data = load_students()
    data[roll] = {"name": str(name).strip(), "gender": str(gender).strip()}
    save_students(data)


def get_student(roll):
    """Retrieve info dictionary for a given roll number."""
    return load_students().get(normalize_roll(roll))


def delete_student(roll, delete_samples: bool = True) -> bool:
    """Delete a student from JSON and optionally remove their captured face samples."""
    roll_str = normalize_roll(roll)
    data = load_students()
    if roll_str not in data:
        return False

    del data[roll_str]
    save_students(data)

    if delete_samples and os.path.exists(DATASET_DIR):
        for folder in os.listdir(DATASET_DIR):
            if folder.startswith(f"{roll_str}_") or folder == roll_str:
                folder_path = os.path.join(DATASET_DIR, folder)
                if os.path.isdir(folder_path):
                    shutil.rmtree(folder_path, ignore_errors=True)

    return True