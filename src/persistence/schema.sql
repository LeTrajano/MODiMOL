CREATE TABLE IF NOT EXISTS molecules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mol_id TEXT,
    smiles_canonico TEXT NOT NULL,
    inchi TEXT,
    inchi_key TEXT UNIQUE,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    molecule_id INTEGER NOT NULL,

    molwt REAL,
    logp REAL,
    tpsa REAL,
    hbd INTEGER,
    hba INTEGER,
    rotbonds INTEGER,
    aromaticrings INTEGER,
    formula TEXT,

    created_at TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (molecule_id) REFERENCES molecules(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS fingerprints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    molecule_id INTEGER NOT NULL,
    fingerprint TEXT NOT NULL,
    nbits INTEGER DEFAULT 2048,
    radius INTEGER DEFAULT 2,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (molecule_id) REFERENCES molecules(id) ON DELETE CASCADE
);