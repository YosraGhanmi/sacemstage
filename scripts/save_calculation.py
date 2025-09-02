import sys
import json
import os
from sqlalchemy.orm import sessionmaker
from setup_database import engine, TransformerCalculation, CalculElectrique, CalculBobinage, CalculThermique, CalculMecanique, CalculGeometrie, CalculCO2, CalculInnovations, CalculNomenclature

def save_calculation_to_db(entrees_json, resultats_json):
    """Sauvegarder un calcul de transformateur dans la base de données avec structure séparée"""
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    try:
        # Parser les données JSON
        entrees = json.loads(entrees_json)
        resultats = json.loads(resultats_json)
        
        nouveau_calcul = TransformerCalculation(
            nom_client=entrees.get('nom_client', ''),
            type_transformateur=entrees.get('type_transformateur', ''),
            reference_projet=entrees.get('nom_projet', ''),
            installation=entrees.get('type_installation', ''),
            puissance_kva=entrees.get('puissance_kva', 0),
            frequence=entrees.get('frequence', 50),
            tension_primaire=entrees.get('tension_primaire', 0),
            tension_secondaire=entrees.get('tension_secondaire', 0),
            variation_pourcent=entrees.get('variation_pourcent', 0),
            couplage=entrees.get('couplage', ''),
            classe_tension=entrees.get('classe_tension', 0),
            densite_courant=entrees.get('densite_courant', 0),
            induction_tesla=entrees.get('induction_tesla', 0),
            tole_magnetique=entrees.get('type_tole', ''),
            nature_bobinage=entrees.get('materiau_enroulement', ''),
            duree_court_circuit=entrees.get('duree_court_circuit', 0),
            pertes_vide=entrees.get('pertes_vide', 0),
            courant_vide_pourcent=entrees.get('courant_vide_pourcent', 0),
            pertes_court_circuit=entrees.get('pertes_court_circuit', 0),
            tension_court_circuit_pourcent=entrees.get('tension_court_circuit_pourcent', 0),
            pertes_totales=entrees.get('pertes_totales', 0),
            echauffement2=entrees.get('temperature', '')
        )
        
        session.add(nouveau_calcul)
        session.flush()  # Pour obtenir l'ID
        
        if 'electrique' in resultats:
            elec = resultats['electrique']
            calcul_elec = CalculElectrique(
                calculation_id=nouveau_calcul.id,
                tension_ligne_primaire=elec.get('tensionLignePrim', 0),
                tension_ligne_secondaire=elec.get('tensionLigneSec', 0),
                tension_phase_primaire=elec.get('tensionPhasePrim', 0),
                tension_phase_secondaire=elec.get('tensionPhaseSec', 0),
                courant_ligne_primaire=elec.get('CourantLignePrim', 0),
                courant_ligne_secondaire=elec.get('CourantLigneSec', 0),
                courant_phase_primaire=elec.get('CourantPhasePrim', 0),
                courant_phase_secondaire=elec.get('CourantPhaseSec', 0),
                pertes_cuivre=elec.get('pertes_cuivre_W', 0),
                pertes_fer=elec.get('pertes_fer_W', 0)
            )
            session.add(calcul_elec)
        
        if 'bobinage' in resultats:
            bob = resultats['bobinage']
            calcul_bob = CalculBobinage(
                calculation_id=nouveau_calcul.id,
                nombre_spires_primaire=bob.get('Nombre de spires primaire', 0),
                nombre_spires_secondaire=bob.get('Nombre de spires secondaire', 0),
                section_conducteur_primaire=bob.get('Section conducteur primaire (mm²)', 0),
                section_conducteur_secondaire=bob.get('Section conducteur secondaire (mm²)', 0),
                densite_courant_primaire=bob.get('DensiteCourantPrim', 0),
                densite_courant_secondaire=bob.get('DensiteCourantSec', 0),
                nombre_couches_primaire=bob.get('N1', 0),
                nombre_couches_secondaire=bob.get('N2', 0)
            )
            session.add(calcul_bob)
        
        if 'thermique' in resultats:
            therm = resultats['thermique']
            calcul_therm = CalculThermique(
                calculation_id=nouveau_calcul.id,
                pertes_totales=therm.get('pertes_totales_W', 0),
                temperature_max=therm.get('echauffement1', 0),
                classe_thermique=therm.get('Classe thermique', ''),
                echauffement2_huile=therm.get('echauffement2', 0),
                echauffement2_cuivre=therm.get('echauffement2', 0)
            )
            session.add(calcul_therm)
        
        if 'mecanique' in resultats:
            meca = resultats['mecanique']
            calcul_meca = CalculMecanique(
                calculation_id=nouveau_calcul.id,
                poids_total=meca.get('Poids total (kg)', 0),
                poids_cuivre=meca.get('MasseTotale', 0),
                poids_fer=meca.get('poids_fer_kg', 0),
                poids_huile=0,
                dimensions_longueur=0,
                dimensions_largeur=0,
                dimensions_hauteur=0
            )
            session.add(calcul_meca)
        
        if 'geometrie' in resultats:
            geom = resultats['geometrie']
            calcul_geom = CalculGeometrie(
                calculation_id=nouveau_calcul.id,
                surface_noyau=geom.get('ColonnesSnette', 0),
                surface_culasse=geom.get('CulasseSnette', 0),
                entrefer=0,
                hauteur_bobine=0,
                diametre_interieur=0,
                diametre_exterieur=0
            )
            session.add(calcul_geom)
        
        if 'co2' in resultats:
            co2 = resultats['co2']
            calcul_co2 = CalculCO2(
                calculation_id=nouveau_calcul.id,
                empreinte_carbone=co2.get('Empreinte carbone (kg CO2)', 0),
                economie_energie=co2.get('Recyclabilité (%)', 0),
                impact_environnemental=''
            )
            session.add(calcul_co2)
        
        if 'innovations' in resultats:
            innov = resultats['innovations']
            calcul_innov = CalculInnovations(
                calculation_id=nouveau_calcul.id,
                technologies_utilisees=innov.get('Efficacité énergétique', ''),
                ameliorations_proposees='',
                innovations_appliquees=str(innov.get('Score innovation', 0))
            )
            session.add(calcul_innov)
        
        if 'nomenclature' in resultats:
            for item in resultats['nomenclature']:
                calcul_nom = CalculNomenclature(
                    calculation_id=nouveau_calcul.id,
                    reference_produit=item.get('composant', ''),
                    designation=item.get('composant', ''),
                    quantite=item.get('quantite', 0),
                    prix_unitaire=item.get('cout_unitaire', 0),
                    prix_total=item.get('cout_total', 0)
                )
                session.add(calcul_nom)

        session.commit()
        
        print(f"Calcul sauvegardé avec ID: {nouveau_calcul.id}")
        return nouveau_calcul.id
        
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la sauvegarde: {e}")
        return None
    finally:
        session.close()

if __name__ == "__main__":
    entrees_json = os.environ.get('ENTREES_JSON', '{}')
    resultats_json = os.environ.get('RESULTATS_JSON', '{}')
    
    if not entrees_json or entrees_json == '{}':
        print("Erreur: Données d'entrée manquantes")
        sys.exit(1)
    
    save_calculation_to_db(entrees_json, resultats_json)
