-- Create database schema for transformer calculations
CREATE TABLE IF NOT EXISTS transformer_calculations (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Input data (French variable names)
    nom_client VARCHAR(255),
    type_transformateur VARCHAR(255),
    installation VARCHAR(255),
    puissance_kva DECIMAL(10,2),
    frequence DECIMAL(10,2),
    tension_primaire DECIMAL(10,2),
    tension_secondaire DECIMAL(10,2),
    variation_pourcent DECIMAL(5,2),
    couplage VARCHAR(50),
    classe_tension DECIMAL(10,2),
    densite_courant DECIMAL(10,4),
    induction_t DECIMAL(10,4),
    tole_magnetique VARCHAR(100),
    nature_bobinage VARCHAR(100),
    duree_cc DECIMAL(10,2),
    pertes_vide_w DECIMAL(10,2),
    i0_vide_pourcent DECIMAL(5,2),
    pcc_w DECIMAL(10,2),
    ucc_pourcent DECIMAL(5,2),
    pertes_totales_w DECIMAL(10,2),
    echauffement2 VARCHAR(50),
    
    -- Calculated results
    masse_cuivre_kg DECIMAL(10,2),
    rendement_ameliore_pourcent DECIMAL(5,2),
    cout_vie_eur DECIMAL(12,2),
    
    -- Additional calculation fields
    tension_ligne_primaire DECIMAL(10,2),
    tension_phase_primaire DECIMAL(10,2),
    courant_ligne_primaire DECIMAL(10,4),
    courant_phase_primaire DECIMAL(10,4),
    tension_ligne_secondaire DECIMAL(10,2),
    tension_phase_secondaire DECIMAL(10,2),
    courant_ligne_secondaire DECIMAL(10,4),
    courant_phase_secondaire DECIMAL(10,4),
    
    -- JSON fields for complex data
    electrique JSONB,
    bobinage JSONB,
    circuit_magnetique JSONB,
    nomenclature JSONB
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_transformer_calculations_created_at ON transformer_calculations(created_at);
CREATE INDEX IF NOT EXISTS idx_transformer_calculations_client ON transformer_calculations(nom_client);
CREATE INDEX IF NOT EXISTS idx_transformer_calculations_puissance ON transformer_calculations(puissance_kva);
