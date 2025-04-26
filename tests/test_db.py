"""
Tests for the database module
"""
import os
import pytest
import tempfile
import sqlite3
from pathlib import Path

from strateplan.db import Database


class TestDatabase:
    """Test suite for the Database class"""
    
    @pytest.fixture
    def temp_db_path(self):
        """Fixture to create a temporary database file path"""
        fd, path = tempfile.mkstemp(suffix=".db")
        yield path
        os.close(fd)
        os.unlink(path)
    
    def test_init(self, temp_db_path):
        """Test database initialization"""
        # Test with explicit path
        db = Database(temp_db_path)
        assert db.db_path == temp_db_path
        assert db.conn is None
        assert db.is_initialized is False
        
        # Test with default path
        db = Database()
        expected_path = Path.home() / ".strateplan" / "strateplan.db"
        assert db.db_path == str(expected_path)
    
    def test_connect(self, temp_db_path):
        """Test database connection"""
        db = Database(temp_db_path)
        db.connect()
        assert db.conn is not None
        assert isinstance(db.conn, sqlite3.Connection)
        db.close()
    
    def test_initialize_db(self, temp_db_path):
        """Test database initialization with tables"""
        db = Database(temp_db_path)
        db.connect()
        db.initialize_db()
        
        # Check that tables were created
        tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
        cursor = db.conn.cursor()
        cursor.execute(tables_query)
        tables = [row[0] for row in cursor.fetchall()]
        
        assert "strategic_plans" in tables
        assert "strategic_issues" in tables
        assert "kpis" in tables
        assert "initiatives" in tables
        assert db.is_initialized is True
        
        db.close()
    
    def test_execute(self, temp_db_path):
        """Test SQL execution"""
        db = Database(temp_db_path)
        db.connect()
        db.initialize_db()
        
        # Execute a test query
        cursor = db.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        assert "strategic_plans" in tables
        db.close()
    
    def test_fetch_all(self, temp_db_path):
        """Test fetching all results"""
        db = Database(temp_db_path)
        db.connect()
        db.initialize_db()
        
        # Insert test data
        db.execute(
            "INSERT INTO strategic_plans (name, description) VALUES (?, ?)",
            ("Test Plan 1", "Description 1")
        )
        db.execute(
            "INSERT INTO strategic_plans (name, description) VALUES (?, ?)",
            ("Test Plan 2", "Description 2")
        )
        db.conn.commit()
        
        # Fetch all test data
        results = db.fetch_all("SELECT * FROM strategic_plans ORDER BY id")
        
        assert len(results) == 2
        assert results[0]["name"] == "Test Plan 1"
        assert results[1]["name"] == "Test Plan 2"
        
        db.close()
    
    def test_fetch_one(self, temp_db_path):
        """Test fetching one result"""
        db = Database(temp_db_path)
        db.connect()
        db.initialize_db()
        
        # Insert test data
        db.execute(
            "INSERT INTO strategic_plans (name, description) VALUES (?, ?)",
            ("Test Plan", "Description")
        )
        db.conn.commit()
        
        # Fetch one test data
        result = db.fetch_one("SELECT * FROM strategic_plans WHERE name = ?", ("Test Plan",))
        
        assert result is not None
        assert result["name"] == "Test Plan"
        assert result["description"] == "Description"
        
        # Test fetching non-existent record
        result = db.fetch_one("SELECT * FROM strategic_plans WHERE name = ?", ("Nonexistent",))
        assert result is None
        
        db.close()
    
    def test_insert(self, temp_db_path):
        """Test inserting data"""
        db = Database(temp_db_path)
        db.connect()
        db.initialize_db()
        
        # Insert test data
        data = {
            "name": "Test Plan",
            "description": "Description",
            "start_date": "2025-01-01",
            "end_date": "2025-12-31",
        }
        
        row_id = db.insert("strategic_plans", data)
        
        assert row_id == 1  # First row should have ID 1
        
        # Verify insertion
        result = db.fetch_one("SELECT * FROM strategic_plans WHERE id = ?", (row_id,))
        
        assert result is not None
        assert result["name"] == "Test Plan"
        assert result["description"] == "Description"
        assert result["start_date"] == "2025-01-01"
        assert result["end_date"] == "2025-12-31"
        
        db.close()
    
    def test_update(self, temp_db_path):
        """Test updating data"""
        db = Database(temp_db_path)
        db.connect()
        db.initialize_db()
        
        # Insert test data
        data = {
            "name": "Test Plan",
            "description": "Description",
        }
        
        row_id = db.insert("strategic_plans", data)
        
        # Update data
        update_data = {
            "name": "Updated Plan",
            "description": "Updated Description",
        }
        
        success = db.update("strategic_plans", row_id, update_data)
        
        assert success is True
        
        # Verify update
        result = db.fetch_one("SELECT * FROM strategic_plans WHERE id = ?", (row_id,))
        
        assert result is not None
        assert result["name"] == "Updated Plan"
        assert result["description"] == "Updated Description"
        
        # Test updating non-existent record
        success = db.update("strategic_plans", 999, update_data)
        assert success is False
        
        db.close()
    
    def test_delete(self, temp_db_path):
        """Test deleting data"""
        db = Database(temp_db_path)
        db.connect()
        db.initialize_db()
        
        # Insert test data
        data = {
            "name": "Test Plan",
            "description": "Description",
        }
        
        row_id = db.insert("strategic_plans", data)
        
        # Delete data
        success = db.delete("strategic_plans", row_id)
        
        assert success is True
        
        # Verify deletion
        result = db.fetch_one("SELECT * FROM strategic_plans WHERE id = ?", (row_id,))
        assert result is None
        
        # Test deleting non-existent record
        success = db.delete("strategic_plans", 999)
        assert success is False
        
        db.close()
