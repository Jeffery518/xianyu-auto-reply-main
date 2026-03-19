import unittest
import sqlite3
import os
import tempfile
import sys
from unittest.mock import patch, MagicMock

# Mock dependencies that might be missing in the environment
mock_modules = ['aiohttp', 'loguru', 'PIL', 'PIL.Image', 'PIL.ImageDraw', 'PIL.ImageFont']
for module_name in mock_modules:
    sys.modules[module_name] = MagicMock()

from db_manager import DBManager

class TestDBManagerSaveCookie(unittest.TestCase):
    def setUp(self):
        # Create a temporary database file to avoid affecting production data
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.db_manager = DBManager(self.db_path)

        # Get admin user ID for reference (it's created in init_db during DBManager init)
        with self.db_manager.lock:
            cursor = self.db_manager.conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = 'admin'")
            res = cursor.fetchone()
            self.admin_id = res[0] if res else 1

    def tearDown(self):
        self.db_manager.close()
        if os.path.exists(self.db_path):
            os.close(self.db_fd)
            os.unlink(self.db_path)

    def test_save_new_cookie_with_explicit_user_id(self):
        """Verify that a new cookie is saved with a provided user_id."""
        cookie_id = "test_cookie_1"
        cookie_value = "value_1"
        user_id = 100

        # Create the user first to satisfy possible foreign key constraints (if enabled)
        with self.db_manager.lock:
            cursor = self.db_manager.conn.cursor()
            cursor.execute("INSERT INTO users (id, username, email, password_hash) VALUES (?, ?, ?, ?)",
                           (user_id, "testuser", "test@example.com", "hash"))
            self.db_manager.conn.commit()

        result = self.db_manager.save_cookie(cookie_id, cookie_value, user_id)
        self.assertTrue(result)

        # Verify the data was saved correctly
        with self.db_manager.lock:
            cursor = self.db_manager.conn.cursor()
            cursor.execute("SELECT id, value, user_id FROM cookies WHERE id = ?", (cookie_id,))
            row = cursor.fetchone()
            self.assertIsNotNone(row)
            self.assertEqual(row[0], cookie_id)
            self.assertEqual(row[1], cookie_value)
            self.assertEqual(row[2], user_id)

    def test_save_new_cookie_defaults_to_admin(self):
        """Verify that a new cookie saved without a user_id defaults to the 'admin' user's ID."""
        cookie_id = "test_cookie_default"
        cookie_value = "value_default"

        result = self.db_manager.save_cookie(cookie_id, cookie_value)
        self.assertTrue(result)

        # Verify it used the admin_id
        with self.db_manager.lock:
            cursor = self.db_manager.conn.cursor()
            cursor.execute("SELECT user_id FROM cookies WHERE id = ?", (cookie_id,))
            row = cursor.fetchone()
            self.assertIsNotNone(row)
            self.assertEqual(row[0], self.admin_id)

    def test_update_existing_cookie_value_preserves_user_id(self):
        """Verify that updating an existing cookie's value without providing a user_id keeps its current user_id."""
        cookie_id = "test_cookie_update"
        initial_value = "initial"
        updated_value = "updated"
        custom_user_id = 200

        # Setup: Create user and initial cookie
        with self.db_manager.lock:
            cursor = self.db_manager.conn.cursor()
            cursor.execute("INSERT INTO users (id, username, email, password_hash) VALUES (?, ?, ?, ?)",
                           (custom_user_id, "user200", "user200@example.com", "hash"))
            self.db_manager.conn.commit()

        self.db_manager.save_cookie(cookie_id, initial_value, custom_user_id)

        # Update value without providing user_id
        result = self.db_manager.save_cookie(cookie_id, updated_value)
        self.assertTrue(result)

        # Verify value changed but user_id is preserved
        with self.db_manager.lock:
            cursor = self.db_manager.conn.cursor()
            cursor.execute("SELECT value, user_id FROM cookies WHERE id = ?", (cookie_id,))
            row = cursor.fetchone()
            self.assertEqual(row[0], updated_value)
            self.assertEqual(row[1], custom_user_id)

    def test_update_existing_cookie_changes_user_id(self):
        """Verify that providing a new user_id when saving an existing cookie ID correctly updates the user_id."""
        cookie_id = "test_cookie_change_user"
        value = "some_value"
        user_id_1 = 301
        user_id_2 = 302

        # Setup: Create users
        with self.db_manager.lock:
            cursor = self.db_manager.conn.cursor()
            cursor.execute("INSERT INTO users (id, username, email, password_hash) VALUES (?, ?, ?, ?)",
                           (user_id_1, "user301", "301@ex.com", "h"))
            cursor.execute("INSERT INTO users (id, username, email, password_hash) VALUES (?, ?, ?, ?)",
                           (user_id_2, "user302", "302@ex.com", "h"))
            self.db_manager.conn.commit()

        self.db_manager.save_cookie(cookie_id, value, user_id_1)

        # Update providing new user_id
        result = self.db_manager.save_cookie(cookie_id, value, user_id_2)
        self.assertTrue(result)

        # Verify user_id changed
        with self.db_manager.lock:
            cursor = self.db_manager.conn.cursor()
            cursor.execute("SELECT user_id FROM cookies WHERE id = ?", (cookie_id,))
            row = cursor.fetchone()
            self.assertEqual(row[0], user_id_2)

    def test_save_cookie_handles_database_exception(self):
        """Verify that save_cookie catches exceptions, rolls back, and returns False."""
        # We can simulate an error by closing the connection or using a mock
        # Mocking DBManager._execute_sql to raise an error
        with patch.object(DBManager, '_execute_sql') as mock_execute:
            mock_execute.side_effect = sqlite3.Error("Simulated DB Error")

            result = self.db_manager.save_cookie("error_cookie", "val")
            self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
