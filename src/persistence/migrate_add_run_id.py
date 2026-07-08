from src.persistence.database import get_connection

def main():
    conn = get_connection()
    try:
        cols = [r["name"] for r in conn.execute("PRAGMA table_info(properties)").fetchall()]
        if "run_id" in cols:
            print("✓ run_id já existe em properties. Nada a fazer.")
            return

        conn.execute("ALTER TABLE properties ADD COLUMN run_id TEXT;")
        conn.execute("UPDATE properties SET run_id = 'legacy' WHERE run_id IS NULL;")
        conn.commit()
        print("✓ Migração concluída: coluna run_id adicionada (legacy para registros antigos).")
    finally:
        conn.close()

if __name__ == "__main__":
    main()