from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime

DATABASE_URL = "postgresql://postgres:root@localhost:5432/sacemcalc"

try:
    engine = create_engine(DATABASE_URL)
    print("Database engine created successfully")
except Exception as e:
    print(f"Error creating database engine: {e}")
    exit(1)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class TransformerCalculation(Base):
    __tablename__ = "transformer_calculations"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Input fields (French names)
    nom_client = Column(String(255))
    reference_projet = Column(String(255))  # Added project reference field
    type_transformateur = Column(String(255))
    installation = Column(String(255))
    puissance_kva = Column(Float)
    frequence = Column(Float)
    tension_primaire = Column(Float)
    tension_secondaire = Column(Float)
    variation_pourcent = Column(Float)
    couplage = Column(String(50))
    classe_tension = Column(Float)
    densite_courant = Column(Float)
    induction_tesla = Column(Float)
    tole_magnetique = Column(String(100))
    nature_bobinage = Column(String(100))
    duree_court_circuit = Column(Float)
    pertes_vide = Column(Float)
    courant_vide_pourcent = Column(Float)
    pertes_court_circuit = Column(Float)
    tension_court_circuit_pourcent = Column(Float)
    pertes_totales = Column(Float)
    echauffement2 = Column(String(50))
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    electrique = relationship("CalculElectrique", back_populates="calculation", uselist=False)
    bobinage = relationship("CalculBobinage", back_populates="calculation", uselist=False)
    thermique = relationship("CalculThermique", back_populates="calculation", uselist=False)
    mecanique = relationship("CalculMecanique", back_populates="calculation", uselist=False)
    geometrie = relationship("CalculGeometrie", back_populates="calculation", uselist=False)
    co2 = relationship("CalculCO2", back_populates="calculation", uselist=False)
    innovations = relationship("CalculInnovations", back_populates="calculation", uselist=False)
    nomenclature = relationship("CalculNomenclature", back_populates="calculation", uselist=False)

class CalculElectrique(Base):
    __tablename__ = "calcul_electrique"
    
    id = Column(Integer, primary_key=True, index=True)
    calculation_id = Column(Integer, ForeignKey("transformer_calculations.id"))
    
    tension_ligne_primaire = Column(Float)
    tension_phase_primaire = Column(Float)
    courant_ligne_primaire = Column(Float)
    courant_phase_primaire = Column(Float)
    tension_ligne_secondaire = Column(Float)
    tension_phase_secondaire = Column(Float)
    courant_ligne_secondaire = Column(Float)
    courant_phase_secondaire = Column(Float)
    pertes_cuivre = Column(Float)
    pertes_fer = Column(Float)
    
    calculation = relationship("TransformerCalculation", back_populates="electrique")

class CalculBobinage(Base):
    __tablename__ = "calcul_bobinage"
    
    id = Column(Integer, primary_key=True, index=True)
    calculation_id = Column(Integer, ForeignKey("transformer_calculations.id"))
    
    nombre_spires_primaire = Column(Integer)
    nombre_spires_secondaire = Column(Integer)
    section_conducteur_primaire = Column(Float)
    section_conducteur_secondaire = Column(Float)
    densite_courant_primaire = Column(Float)
    densite_courant_secondaire = Column(Float)
    nombre_couches_primaire = Column(Integer)
    nombre_couches_secondaire = Column(Integer)
    
    calculation = relationship("TransformerCalculation", back_populates="bobinage")

class CalculThermique(Base):
    __tablename__ = "calcul_thermique"
    
    id = Column(Integer, primary_key=True, index=True)
    calculation_id = Column(Integer, ForeignKey("transformer_calculations.id"))
    
    pertes_totales = Column(Float)
    temperature_max = Column(Float)
    classe_thermique = Column(String(50))
    echauffement2_huile = Column(Float)
    echauffement2_cuivre = Column(Float)
    
    calculation = relationship("TransformerCalculation", back_populates="thermique")

class CalculMecanique(Base):
    __tablename__ = "calcul_mecanique"
    
    id = Column(Integer, primary_key=True, index=True)
    calculation_id = Column(Integer, ForeignKey("transformer_calculations.id"))
    
    poids_total = Column(Float)
    poids_cuivre = Column(Float)
    poids_fer = Column(Float)
    poids_huile = Column(Float)
    dimensions_longueur = Column(Float)
    dimensions_largeur = Column(Float)
    dimensions_hauteur = Column(Float)
    
    calculation = relationship("TransformerCalculation", back_populates="mecanique")

class CalculGeometrie(Base):
    __tablename__ = "calcul_geometrie"
    
    id = Column(Integer, primary_key=True, index=True)
    calculation_id = Column(Integer, ForeignKey("transformer_calculations.id"))
    
    surface_noyau = Column(Float)
    surface_culasse = Column(Float)
    entrefer = Column(Float)
    hauteur_bobine = Column(Float)
    diametre_interieur = Column(Float)
    diametre_exterieur = Column(Float)
    
    calculation = relationship("TransformerCalculation", back_populates="geometrie")

class CalculCO2(Base):
    __tablename__ = "calcul_co2"
    
    id = Column(Integer, primary_key=True, index=True)
    calculation_id = Column(Integer, ForeignKey("transformer_calculations.id"))
    
    empreinte_carbone = Column(Float)
    economie_energie = Column(Float)
    impact_environnemental = Column(String(255))
    
    calculation = relationship("TransformerCalculation", back_populates="co2")

class CalculInnovations(Base):
    __tablename__ = "calcul_innovations"
    
    id = Column(Integer, primary_key=True, index=True)
    calculation_id = Column(Integer, ForeignKey("transformer_calculations.id"))
    
    technologies_utilisees = Column(Text)
    ameliorations_proposees = Column(Text)
    innovations_appliquees = Column(Text)
    
    calculation = relationship("TransformerCalculation", back_populates="innovations")

class CalculNomenclature(Base):
    __tablename__ = "calcul_nomenclature"
    
    id = Column(Integer, primary_key=True, index=True)
    calculation_id = Column(Integer, ForeignKey("transformer_calculations.id"))
    
    reference_produit = Column(String(255))
    designation = Column(String(255))
    quantite = Column(Integer)
    prix_unitaire = Column(Float)
    prix_total = Column(Float)
    
    calculation = relationship("TransformerCalculation", back_populates="nomenclature")

# Create all tables
try:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    print("Tables created:")
    print("- transformer_calculations")
    print("- calcul_electrique")
    print("- calcul_bobinage") 
    print("- calcul_thermique")
    print("- calcul_mecanique")
    print("- calcul_geometrie")
    print("- calcul_co2")
    print("- calcul_innovations")
    print("- calcul_nomenclature")
except Exception as e:
    print(f"Error creating tables: {e}")
