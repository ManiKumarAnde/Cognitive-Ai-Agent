import sqlite3

class SQLiteMemory:
    def __init__(self, db_file="memory.db"):
        self.conn = sqlite3.connect(db_file)
        self._create_table()

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS memory (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def store(self, key, value):
        query = """
        INSERT OR REPLACE INTO memory (key, value)
        VALUES (?, ?)
        """
        self.conn.execute(query, (key, value))
        self.conn.commit()

    def recall(self, key):
        cursor = self.conn.execute(
            "SELECT value FROM memory WHERE key = ?", (key,)
        )
        row = cursor.fetchone()
        return row[0] if row else None

    def close(self):
        self.conn.close()
