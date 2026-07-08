from src.persistence.database import get_connection

def main():
    conn = get_connection()
    try:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            source TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            notes TEXT
        );
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_runs_created_at ON runs(created_at);")
        conn.commit()
        print("✓ Tabela runs criada/confirmada.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()