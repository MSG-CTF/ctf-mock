from pathlib import Path
from unittest import TestCase

ROOT_DIR = Path(__file__).resolve().parents[1]


class ProjectBootstrapTests(TestCase):
    def test_django_project_files_exist(self):
        expected_files = [
            "manage.py",
            "requirements.txt",
            "config/settings.py",
            "config/urls.py",
            "mock_api/apps.py",
            "mock_api/urls.py",
            "mock_api/views.py",
        ]

        missing_files = [
            file_path
            for file_path in expected_files
            if not (ROOT_DIR / file_path).exists()
        ]

        self.assertEqual(missing_files, [])

    def test_readme_contains_django_run_command(self):
        readme = (ROOT_DIR / "README.md").read_text(encoding="utf-8")
        self.assertIn("python manage.py runserver", readme)
