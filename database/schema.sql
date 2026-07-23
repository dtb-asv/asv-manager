-- =========================================================
-- ASV Neufeld Manager
-- PostgreSQL Grundstruktur
-- =========================================================


-- ---------------------------------------------------------
-- Saisonen
-- ---------------------------------------------------------

CREATE TABLE IF NOT EXISTS seasons (
    season_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE,
    start_date DATE,
    end_date DATE,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ---------------------------------------------------------
-- Personen
-- Eine Person wird nur einmal gespeichert.
-- ---------------------------------------------------------

CREATE TABLE IF NOT EXISTS persons (
    person_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    external_member_id INTEGER,

    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    birth_date DATE,

    active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_person_identity
        UNIQUE (first_name, last_name, birth_date)
);


-- ---------------------------------------------------------
-- Mitgliedschaften
-- Eine Person kann in mehreren Saisonen Mitglied sein.
-- ---------------------------------------------------------

CREATE TABLE IF NOT EXISTS memberships (
    membership_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    person_id BIGINT NOT NULL
        REFERENCES persons(person_id)
        ON DELETE CASCADE,

    season_id BIGINT NOT NULL
        REFERENCES seasons(season_id)
        ON DELETE RESTRICT,

    status VARCHAR(30) NOT NULL DEFAULT 'aktiv',

    joined_on DATE,
    left_on DATE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_membership_person_season
        UNIQUE (person_id, season_id)
);


-- ---------------------------------------------------------
-- Mannschaften
-- ---------------------------------------------------------

CREATE TABLE IF NOT EXISTS teams (
    team_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    season_id BIGINT NOT NULL
        REFERENCES seasons(season_id)
        ON DELETE RESTRICT,

    name VARCHAR(50) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_team_season
        UNIQUE (season_id, name)
);


-- ---------------------------------------------------------
-- Orte und Sportplätze
-- ---------------------------------------------------------

CREATE TABLE IF NOT EXISTS places (
    place_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    name VARCHAR(150) NOT NULL UNIQUE,
    address VARCHAR(250),

    active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ---------------------------------------------------------
-- Spiele
-- ---------------------------------------------------------

CREATE TABLE IF NOT EXISTS games (
    game_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    season_id BIGINT NOT NULL
        REFERENCES seasons(season_id)
        ON DELETE RESTRICT,

    team_id BIGINT NOT NULL
        REFERENCES teams(team_id)
        ON DELETE RESTRICT,

    place_id BIGINT
        REFERENCES places(place_id)
        ON DELETE SET NULL,

    round_number INTEGER,

    game_date DATE NOT NULL,
    start_time TIME,
    end_time TIME,

    opponent VARCHAR(150) NOT NULL,

    home_away VARCHAR(20) NOT NULL,
    game_type VARCHAR(50) NOT NULL DEFAULT 'Meisterschaftsspiel',
    status VARCHAR(30) NOT NULL DEFAULT 'aktiv',

    notes TEXT,

    source_file VARCHAR(250),
    source_sheet VARCHAR(100),
    source_row INTEGER,
    source_key VARCHAR(150),

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_game_home_away
        CHECK (home_away IN ('Heim', 'Auswärts', 'Neutral')),

    CONSTRAINT uq_game_source
        UNIQUE (source_key)
);


-- ---------------------------------------------------------
-- Teamzuordnungen
-- Ein Mitglied kann einer oder mehreren Mannschaften
-- zugeordnet werden.
-- ---------------------------------------------------------

CREATE TABLE IF NOT EXISTS team_members (
    team_member_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    team_id BIGINT NOT NULL
        REFERENCES teams(team_id)
        ON DELETE CASCADE,

    person_id BIGINT NOT NULL
        REFERENCES persons(person_id)
        ON DELETE CASCADE,

    role VARCHAR(30) NOT NULL DEFAULT 'Spieler',

    valid_from DATE,
    valid_until DATE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_team_member
        UNIQUE (team_id, person_id, role)
);


-- ---------------------------------------------------------
-- Importvorgänge
-- Damit später nachvollziehbar bleibt, wann welche
-- Excel-Datei eingelesen wurde.
-- ---------------------------------------------------------

CREATE TABLE IF NOT EXISTS import_batches (
    import_batch_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    import_type VARCHAR(50) NOT NULL,
    source_file VARCHAR(250) NOT NULL,

    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    finished_at TIMESTAMP,

    rows_read INTEGER NOT NULL DEFAULT 0,
    rows_created INTEGER NOT NULL DEFAULT 0,
    rows_updated INTEGER NOT NULL DEFAULT 0,
    rows_skipped INTEGER NOT NULL DEFAULT 0,
    rows_failed INTEGER NOT NULL DEFAULT 0,

    status VARCHAR(30) NOT NULL DEFAULT 'gestartet',
    report TEXT
);


-- ---------------------------------------------------------
-- Erste Saison anlegen
-- ---------------------------------------------------------

INSERT INTO seasons (
    name,
    start_date,
    end_date,
    active
)
VALUES (
    '2026/27',
    DATE '2026-07-01',
    DATE '2027-06-30',
    TRUE
)
ON CONFLICT (name) DO NOTHING;


-- ---------------------------------------------------------
-- Hilfreiche Indizes
-- ---------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_persons_name
    ON persons(last_name, first_name);

CREATE INDEX IF NOT EXISTS idx_persons_birth_date
    ON persons(birth_date);

CREATE INDEX IF NOT EXISTS idx_games_date
    ON games(game_date);

CREATE INDEX IF NOT EXISTS idx_games_team
    ON games(team_id);

CREATE INDEX IF NOT EXISTS idx_memberships_season
    ON memberships(season_id);