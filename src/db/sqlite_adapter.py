"""SQLite database adapter"""
import sqlite3
from typing import List, Dict, Any
from pathlib import Path

class SQLiteAdapter:
    """Adapter for SQLite databases"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        """Connect to database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return self
    
    def close(self):
        """Close connection"""
        if self.conn:
            self.conn.close()
    
    def get_tables(self) -> List[str]:
        """Get all table names"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        return [row[0] for row in cursor.fetchall()]
    
    def get_schema(self, table_name: str) -> Dict[str, Any]:
        """Get schema for a specific table"""
        cursor = self.conn.cursor()
        
        # Get columns
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = []
        for row in cursor.fetchall():
            columns.append({
                'name': row[1],
                'type': row[2],
                'nullable': not row[3],
                'primary_key': bool(row[5])
            })
        
        # Get foreign keys
        cursor.execute(f"PRAGMA foreign_key_list({table_name})")
        foreign_keys = []
        for row in cursor.fetchall():
            foreign_keys.append({
                'column': row[3],
                'references_table': row[2],
                'references_column': row[4]
            })
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        
        return {
            'table_name': table_name,
            'columns': columns,
            'foreign_keys': foreign_keys,
            'row_count': row_count
        }
    
    def get_full_schema(self) -> Dict[str, Any]:
        """Get schema for all tables"""
        tables = self.get_tables()
        return {
            table: self.get_schema(table)
            for table in tables
        }
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results"""
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        
        # Convert rows to dictionaries
        columns = [description[0] for description in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        return results
    
    #allows for with statement to be called automatically
    def __enter__(self):
        return self.connect()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()