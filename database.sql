CREATE TABLE IF NOT EXISTS grupos (
    id SERIAL PRIMARY KEY,
    numero_grupo INTEGER UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS grupo_miembros (
    id SERIAL PRIMARY KEY,
    numero_grupo INTEGER REFERENCES grupos(numero_grupo) ON DELETE CASCADE,
    user_id BIGINT NOT NULL,
    username VARCHAR(255) NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(numero_grupo, user_id)
);
