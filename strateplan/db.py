"""
Database module for Strategic Plan CLI
"""
import os
import sqlite3
import pathlib
from typing import Optional, List, Dict, Any, Tuple, Union


class Database:
    """SQLite Database management class"""

    def __init__(self, db_path: Optional[str] = None):
        """Initialize database connection

        Args:
            db_path: Path to SQLite database file. If None, uses default path.
        """
        if db_path is None:
            # Use default path - in user's home directory
            home_dir = pathlib.Path.home()
            db_dir = home_dir / ".strateplan"
            db_dir.mkdir(exist_ok=True)
            db_path = str(db_dir / "strateplan.db")

        self.db_path = db_path
        self.conn = None
        self.is_initialized = False

    def connect(self) -> None:
        """Connect to the SQLite database"""
        self.conn = sqlite3.connect(self.db_path)
        # Enable foreign keys
        self.conn.execute("PRAGMA foreign_keys = ON")
        # Return rows as dictionaries
        self.conn.row_factory = sqlite3.Row

    def close(self) -> None:
        """Close the database connection"""
        if self.conn:
            self.conn.close()

    def initialize_db(self) -> None:
        """Create database tables if they don't exist"""
        if self.is_initialized:
            return

        # Connect to database
        if not self.conn:
            self.connect()
        
        # Define SQL statements to create tables
        strategic_plans_table = """
        CREATE TABLE IF NOT EXISTS strategic_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            start_date TEXT,
            end_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        strategic_issues_table = """
        CREATE TABLE IF NOT EXISTS strategic_issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plan_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            priority INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (plan_id) REFERENCES strategic_plans (id) ON DELETE CASCADE
        );
        """
        
        kpis_table = """
        CREATE TABLE IF NOT EXISTS kpis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            target_value REAL,
            current_value REAL,
            unit TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (issue_id) REFERENCES strategic_issues (id) ON DELETE CASCADE
        );
        """
        
        initiatives_table = """
        CREATE TABLE IF NOT EXISTS initiatives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            status TEXT,
            budget REAL,
            start_date TEXT,
            end_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (issue_id) REFERENCES strategic_issues (id) ON DELETE CASCADE
        );
        """
        
        # Execute SQL statements
        cursor = self.conn.cursor()
        cursor.execute(strategic_plans_table)
        cursor.execute(strategic_issues_table)
        cursor.execute(kpis_table)
        cursor.execute(initiatives_table)
        self.conn.commit()
        
        self.is_initialized = True

    def execute(self, query: str, params: Tuple = ()) -> sqlite3.Cursor:
        """Execute a SQL query with parameters
        
        Args:
            query: SQL query to execute
            params: Parameters for the SQL query
            
        Returns:
            sqlite3.Cursor: Cursor for the executed query
        """
        if not self.conn:
            self.connect()
            
        if not self.is_initialized:
            self.initialize_db()
            
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor

    def fetch_all(self, query: str, params: Tuple = ()) -> List[Dict[str, Any]]:
        """Execute a query and fetch all results as dictionaries
        
        Args:
            query: SQL query to execute
            params: Parameters for the SQL query
            
        Returns:
            List of dictionaries containing the query results
        """
        cursor = self.execute(query, params)
        results = cursor.fetchall()
        return [dict(row) for row in results]

    def fetch_one(self, query: str, params: Tuple = ()) -> Optional[Dict[str, Any]]:
        """Execute a query and fetch one result as dictionary
        
        Args:
            query: SQL query to execute
            params: Parameters for the SQL query
            
        Returns:
            Dictionary containing the result or None if no result
        """
        cursor = self.execute(query, params)
        result = cursor.fetchone()
        return dict(result) if result else None

    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """Insert data into a table
        
        Args:
            table: Table name
            data: Dictionary of column names and values
            
        Returns:
            The ID of the inserted row
        """
        if not self.conn:
            self.connect()
            
        if not self.is_initialized:
            self.initialize_db()
            
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        values = tuple(data.values())
        
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        
        return cursor.lastrowid

    def update(self, table: str, id_value: int, data: Dict[str, Any], id_column: str = "id") -> bool:
        """Update data in a table
        
        Args:
            table: Table name
            id_value: Value of the ID column
            data: Dictionary of column names and values to update
            id_column: Name of the ID column
            
        Returns:
            True if successful, False otherwise
        """
        if not data:
            return False
            
        if not self.conn:
            self.connect()
            
        set_clause = ", ".join([f"{column} = ?" for column in data.keys()])
        values = tuple(data.values()) + (id_value,)
        
        query = f"UPDATE {table} SET {set_clause} WHERE {id_column} = ?"
        
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        
        return cursor.rowcount > 0

    def delete(self, table: str, id_value: int, id_column: str = "id") -> bool:
        """Delete data from a table
        
        Args:
            table: Table name
            id_value: Value of the ID column
            id_column: Name of the ID column
            
        Returns:
            True if successful, False otherwise
        """
        if not self.conn:
            self.connect()
            
        query = f"DELETE FROM {table} WHERE {id_column} = ?"
        
        cursor = self.conn.cursor()
        cursor.execute(query, (id_value,))
        self.conn.commit()
        
        return cursor.rowcount > 0


# Singleton instance of the database
_db_instance = None

def get_db() -> Database:
    """Get singleton instance of the database
    
    Returns:
        Database instance
    """
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
        _db_instance.connect()
        _db_instance.initialize_db()
    return _db_instance
