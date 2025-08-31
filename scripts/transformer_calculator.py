import json
import os
import sys
import math
from typing import Dict, Any, List

class TransformerCalculator:
    def __init__(self, entrees: Dict[str, Any]):
        self.entrees = entrees
        
        self.RESISTIVITY_CU = 1.724e-8  # Ω·m at 20°C
        self.RESISTIVITY_AL = 2.82e-8   # Ω·m at 20°C
        self.TEMP_COEFF_RESISTIVITY = 0.00393
        self.DENSITY_CU = 8900  # kg/m³
        self.DENSITY_AL = 2700  # kg/m³
        self.STACKING_FACTOR = 0.9
        
        self.CORE_LOSS_TABLE = {
            "0.27mm": 0.85,
            "0.30mm": 0.95,
            "0.35mm": 1.1,
            "HiB": 0.75,
        }

    def calculer_tout(self) -> Dict[str, Any]:
        try:
            electrique = self.calculer_electrique()
            bobinage = self.calculer_bobinage()
            thermique = self.calculer_thermique()
            mecanique = self.calculer_mecanique()
            geometrie = self.calculer_geometrie()
            
            return {
                "electrique": electrique,
                "bobinage": bobinage,
                "thermique": thermique,
                "mecanique": mecanique,
                "geometrie": geometrie,
                "masse_cuivre_kg": self.calculer_poids_cuivre(),
                "rendement_ameliore_pourcent": self.calculer_rendement(),
                "cout_vie_eur": self.calculer_cout_vie(),
                "co2": self.calculer_impact_co2(),
                "nomenclature": self.calculer_nomenclature(),
                "cout_nomenclature": self.calculer_cout_nomenclature(),
                "classe_refroidissement_suggeree": self.suggerer_classe_refroidissement(),
                "success": True
            }
        except Exception as e:
            return {
                "error": f"Calculation error: {str(e)}",
                "success": False
            }

    def calculer_electrique(self) -> Dict[str, Any]:
        puissance_kva = self.entrees.get("puissance_kva", 0)
        tension_primaire = self.entrees.get("tension_primaire", 0)
        tension_secondaire = self.entrees.get("tension_secondaire", 0)

        if not all([puissance_kva, tension_primaire, tension_secondaire]):
            raise ValueError("Missing required fields: puissance_kva, tension_primaire, tension_secondaire")

        courant_prim = self.calculer_courant_ligne_primaire()
        courant_sec = self.calculer_courant_ligne_secondaire()

        tension_phase_prim = self.calculer_tension_phase_primaire()
        tension_phase_sec = self.calculer_tension_phase_secondaire()

        pertes_cuivre = self.calculer_pertes_cuivre()
        pertes_fer = self.calculer_pertes_fer()

        return {
            "tensionLignePrim": tension_primaire,
            "tensionLigneSec": tension_secondaire,
            "tensionPhasePrim": tension_phase_prim,
            "tensionPhaseSec": tension_phase_sec,
            "CourantLignePrim": courant_prim,
            "CourantLigneSec": courant_sec,
            "CourantPhasePrim": courant_prim,
            "CourantPhaseSec": courant_sec,
            "ClasseTensionPrim": self.calculer_classe_tension_primaire(),
            "ClasseTensionSec": self.calculer_classe_tension_secondaire(),
            "classeTensionlast": self.obtenir_classe_tension(max(tension_primaire, tension_secondaire)),
            "pertes_cuivre_W": pertes_cuivre,
            "pertes_fer_W": pertes_fer,
        }

    def calculer_bobinage(self) -> Dict[str, Any]:
        tension_primaire = self.entrees["tension_primaire"]
        tension_secondaire = self.entrees["tension_secondaire"]

        volts_par_spire = self.calculer_volts_par_spire()
        rapport_spires = tension_primaire / tension_secondaire
        nombre_spires_prim = self.calculer_nombre_spires_primaire()
        nombre_spires_sec = self.calculer_nombre_spires_secondaire()

        section_conducteur_prim = self.calculer_section_conducteur_primaire()
        section_conducteur_sec = self.calculer_section_conducteur_secondaire()

        return {
            "Nombre de spires primaire": nombre_spires_prim,
            "Nombre de spires secondaire": nombre_spires_sec,
            "Section conducteur primaire (mm²)": section_conducteur_prim,
            "Section conducteur secondaire (mm²)": section_conducteur_sec,
            "spiresVsp": volts_par_spire,
            "N1": nombre_spires_prim,
            "N2": nombre_spires_sec,
            "BobSectionduConducteurprim1": section_conducteur_prim,
            "BobSectionduConducteurSec": section_conducteur_sec,
            "DensiteCourantPrim": self.calculer_densite_courant_primaire(),
            "DensiteCourantSec": self.calculer_densite_courant_secondaire(),
        }

    def calculer_thermique(self) -> Dict[str, Any]:
        pertes_totales = self.calculer_pertes_totales()
        temperature_max = self.calculer_temperature_max()

        return {
            "pertes_totales_W": pertes_totales,
            "Température max (°C)": round(temperature_max),
            "Classe thermique": self.obtenir_classe_thermique(temperature_max),
            "Echauffement": self.calculer_echauffement(),
        }

    def calculer_mecanique(self) -> Dict[str, Any]:
        poids_total_kg = self.calculer_poids_total_kg()
        dimensions = self.calculer_dimensions(self.entrees["puissance_kva"])

        return {
            "Poids total (kg)": round(poids_total_kg),
            "Dimensions (mm)": dimensions,
            "MasseTotale": round(poids_total_kg),
        }

    def calculer_geometrie(self) -> Dict[str, Any]:
        puissance_kva = self.entrees["puissance_kva"]
        b_max = self.entrees["b_max"]

        poids_fer = self.calculer_poids_fer()
        surface_noyau = puissance_kva * 15

        return {
            "poids_fer_kg": round(poids_fer * 10) / 10,
            "ColonnesSnette": surface_noyau,
            "ColonnesBT": b_max,
            "ColonnesMasse": poids_fer * 0.6,
            "4emeColonneSnette": surface_noyau * 0.8,
            "4emeColonneMasse": poids_fer * 0.2,
            "CulasseSnette": surface_noyau * 1.2,
            "CulasseBT": b_max * 0.9,
            "CulasseMasse": poids_fer * 0.4,
            "EPCM": 0.35,
            "MasseCulplusCol": poids_fer,
            "MasseTotale": poids_fer,
        }

    def calculer_impact_co2(self) -> Dict[str, Any]:
        puissance_kva = self.entrees["puissance_kva"]
        empreinte = puissance_kva * 1.25
        return {
            "Empreinte carbone (kg CO2)": round(empreinte * 10) / 10,
            "Recyclabilité (%)": 85,
        }

    def calculer_innovations(self) -> Dict[str, Any]:
        rendement = self.calculer_rendement()
        return {
            "Efficacité énergétique": "Classe A+" if rendement > 97 else ("Classe A" if rendement > 95 else "Classe B"),
            "Score innovation": round((rendement - 90) * 10) / 10,
        }

    def calculer_nomenclature(self) -> List[Dict[str, Any]]:
        puissance_kva = self.entrees.get("puissance_kva", self.entrees.get("power_kva", 100))
        materiau_enroulement = self.entrees.get("materiau_enroulement", self.entrees.get("winding_material", "cuivre"))
        prix_cuivre = 8.5 if materiau_enroulement == "cuivre" else 6.2
        
        return [
            {
                "composant": "Noyau magnétique",
                "quantite": 1,
                "cout_unitaire": puissance_kva * 4.5,
                "cout_total": puissance_kva * 4.5,
            },
            {
                "composant": f"{materiau_enroulement} primaire",
                "quantite": round(puissance_kva * 0.25),
                "cout_unitaire": prix_cuivre,
                "cout_total": round(puissance_kva * 0.25 * prix_cuivre * 100) / 100,
            },
            {
                "composant": f"{materiau_enroulement} secondaire",
                "quantite": round(puissance_kva * 0.2),
                "cout_unitaire": prix_cuivre,
                "cout_total": round(puissance_kva * 0.2 * prix_cuivre * 100) / 100,
            },
            {
                "composant": "Isolation",
                "quantite": 1,
                "cout_unitaire": puissance_kva * 0.85,
                "cout_total": puissance_kva * 0.85,
            },
        ]

    def calculer_cout_nomenclature(self) -> float:
        return sum(item["cout_total"] for item in self.calculer_nomenclature())

    def calculer_cout_vie(self) -> int:
        puissance_kva = self.entrees["puissance_kva"]
        cout_initial = self.calculer_cout_nomenclature()
        cout_fonctionnement = puissance_kva * 15 * 20
        return round(cout_initial + cout_fonctionnement)

    def suggerer_classe_refroidissement(self) -> str:
        puissance_kva = self.entrees["puissance_kva"]
        type_refroidissement = self.entrees.get("type_refroidissement")
        
        if type_refroidissement:
            return type_refroidissement
        if puissance_kva <= 100:
            return "AN"
        if puissance_kva <= 500:
            return "ONAN"
        if puissance_kva <= 1000:
            return "ONAN+"
        return "ONAF"

    # Calculation methods
    def calculer_tension_phase_primaire(self) -> float:
        return self.entrees["tension_primaire"] / math.sqrt(3)

    def calculer_tension_phase_secondaire(self) -> float:
        return self.entrees["tension_secondaire"] / math.sqrt(3)

    def calculer_courant_ligne_primaire(self) -> float:
        return (self.entrees["puissance_kva"] * 1000) / (self.entrees["tension_primaire"] * math.sqrt(3))

    def calculer_courant_ligne_secondaire(self) -> float:
        return (self.entrees["puissance_kva"] * 1000) / (self.entrees["tension_secondaire"] * math.sqrt(3))

    def calculer_classe_tension_primaire(self) -> str:
        return self.obtenir_classe_tension(self.entrees["tension_primaire"])

    def calculer_classe_tension_secondaire(self) -> str:
        return self.obtenir_classe_tension(self.entrees["tension_secondaire"])

    def calculer_nombre_spires_primaire(self) -> int:
        volts_par_spire = self.calculer_volts_par_spire()
        return round(self.entrees["tension_primaire"] / volts_par_spire)

    def calculer_nombre_spires_secondaire(self) -> int:
        rapport_spires = self.entrees["tension_primaire"] / self.entrees["tension_secondaire"]
        return round(self.calculer_nombre_spires_primaire() / rapport_spires)

    def calculer_volts_par_spire(self) -> float:
        tension_primaire = self.entrees.get("tension_primaire", 0)
        frequence_hz = self.entrees.get("frequence_hz", 50)  # Default to 50Hz
        b_max = self.entrees.get("b_max", 1.5)  # Default B_max
        
        if frequence_hz == 0 or b_max == 0:
            return 1.0  # Safe default value
            
        return tension_primaire / (4.44 * frequence_hz * b_max * 1e-4 * math.sqrt(3))

    def calculer_section_conducteur_primaire(self) -> float:
        return self.calculer_section_conducteur(
            self.entrees["puissance_kva"],
            self.entrees["tension_primaire"],
            self.entrees["materiau_enroulement"],
        )

    def calculer_section_conducteur_secondaire(self) -> float:
        return self.calculer_section_conducteur(
            self.entrees["puissance_kva"],
            self.entrees["tension_secondaire"],
            self.entrees["materiau_enroulement"],
        )

    def calculer_densite_courant_primaire(self) -> float:
        courant = self.calculer_courant_ligne_primaire()
        section = self.calculer_section_conducteur_primaire()
        return courant / section

    def calculer_densite_courant_secondaire(self) -> float:
        courant = self.calculer_courant_ligne_secondaire()
        section = self.calculer_section_conducteur_secondaire()
        return courant / section

    def calculer_pertes_cuivre(self) -> float:
        courant_prim = self.calculer_courant_ligne_primaire()
        courant_sec = self.calculer_courant_ligne_secondaire()
        return pow(courant_prim, 2) * 0.5 + pow(courant_sec, 2) * 0.3

    def calculer_pertes_fer(self) -> float:
        return self.entrees["puissance_kva"] * 0.8

    def calculer_pertes_totales(self) -> float:
        return self.calculer_pertes_cuivre() + self.calculer_pertes_fer()

    def calculer_temperature_max(self) -> float:
        pertes_totales = self.calculer_pertes_totales()
        return 75 + (pertes_totales / self.entrees["puissance_kva"]) * 0.05

    def calculer_echauffement(self) -> int:
        return round(self.calculer_temperature_max() - 40)

    def calculer_poids_total_kg(self) -> float:
        return self.entrees["puissance_kva"] * 1.8 + 50

    def calculer_poids_cuivre(self) -> float:
        return round(self.entrees["puissance_kva"] * 0.45 * 10) / 10

    def calculer_poids_fer(self) -> float:
        return self.entrees["puissance_kva"] * 0.95

    def calculer_rendement(self) -> float:
        pertes = self.entrees["puissance_kva"] * 12
        rendement = (1 - pertes / (self.entrees["puissance_kva"] * 1000)) * 100
        return round(rendement * 100) / 100

    # Utility methods
    def obtenir_classe_tension(self, tension: float) -> str:
        if tension >= 24000:
            return "36"
        if tension >= 17500:
            return "24"
        if tension >= 12000:
            return "17.5"
        if tension >= 7600:
            return "12"
        if tension >= 3600:
            return "7.2"
        if tension >= 1100:
            return "3.6"
        return "1.1"

    def obtenir_classe_thermique(self, temp: float) -> str:
        if temp <= 105:
            return "A"
        if temp <= 120:
            return "E"
        if temp <= 130:
            return "B"
        if temp <= 155:
            return "F"
        return "H"

    def calculer_section_conducteur(self, puissance: float, tension: float, materiau: str) -> float:
        courant = (puissance * 1000) / (tension * math.sqrt(3))
        densite = 3.5 if materiau == "cuivre" else 2.5
        return round((courant / densite) * 100) / 100

    def calculer_dimensions(self, puissance: float) -> str:
        longueur = round(300 + puissance * 0.8)
        largeur = round(250 + puissance * 0.6)
        hauteur = round(400 + puissance * 0.5)
        return f"{longueur}x{largeur}x{hauteur}"


def main():
    try:
        entrees_json = os.environ.get('ENTREES_JSON')
        if not entrees_json:
            result = {"error": "ENTREES_JSON environment variable not set", "success": False}
            print(json.dumps(result))
            return
        
        try:
            entrees = json.loads(entrees_json)
        except json.JSONDecodeError as e:
            result = {"error": f"Invalid JSON in ENTREES_JSON: {str(e)}", "success": False}
            print(json.dumps(result))
            return
        
        calculator = TransformerCalculator(entrees)
        results = calculator.calculer_tout()
        
        if "error" not in results:
            results["success"] = True
            
        print(json.dumps(results))
        
    except Exception as e:
        error_result = {"error": f"Unexpected error: {str(e)}", "success": False}
        print(json.dumps(error_result))

if __name__ == "__main__":
    main()
