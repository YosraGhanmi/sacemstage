import json
import os
import sys
import math
from typing import Dict, Any, List

class TransformerCalculator:
    def __init__(self, entrees: Dict[str, Any]):
        self.entrees = entrees
        self.couplage = self.entrees["couplage_primaire"]+self.entrees["couplage_secondaire"]+self.entrees["indice_horaire"]
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
        self.garanties1 = [
            [25,   140, 3.30,   700,   4.00],
            [40,   190, 3.00,   900,   4.00],
            [50,   220, 2.90,  1320,   4.00],
            [63,   235, 2.80,  1500,   4.00],
            [75,   285, 2.70,  1650,   4.00],
            [80,   320, 2.60,  1800,   4.00],
            [100,  330, 2.50,  2100,   4.00],
            [125,  400, 2.40,  2250,   4.00],
            [160,  530, 2.30,  2600,   4.00],
            [200,  570, 2.20,  3000,   4.00],
            [250,  600, 2.10,  3800,   4.00],
            [300,  780, 2.00,  4300,   4.00],
            [315,  840, 2.00,  4400,   4.00],
            [400,  930, 1.90,  5100,   4.00],
            [500, 1180, 1.90,  6000,   4.00],
            [630, 1320, 1.80,  7900,   4.00],
            [800, 1600, 2.00, 12000,   4.50],
            [1000,1800, 2.40, 13300,   5.00],
            [1250,2160, 2.20, 17600,   5.00],
            [1600,2540, 2.00, 20500,   5.50],
            [2000,3300, 1.90, 26000,   6.50],
            [2500,3680, 1.80, 29000,   7.00],
            [3150,4360, 1.70, 35000,   7.00]
            ]
        # Matrix as list of lists
        self.garanties2 = [
            [25,   190, 7.90,   800,   4.50],
            [40,   230, 6.30,   870,   4.50],
            [50,   260, 5.00,  1450,   4.50],
            [63,   300, 4.80,  1640,   4.50],
            [80,   360, 4.50,  1980,   4.50],
            [100,  400, 4.40,  2340,   4.50],
            [125,  460, 4.10,  2790,   4.50],
            [160,  530, 3.90,  3330,   4.50],
            [200,  600, 3.70,  3980,   4.50],
            [250,  750, 3.50,  4230,   4.50],
            [315,  920, 3.20,  5200,   4.50],
            [400, 1160, 3.20,  6210,   4.50],
            [500, 1310, 3.10,  7400,   4.50],
            [630, 1600, 2.90,  8820,   4.50],
            [800, 1800, 2.80, 12500,   5.00],
            [1000,2200, 2.70, 14000,   5.50],
            [1250,2500, 2.50, 18500,   6.00],
            [1600,2900, 2.20, 21500,   6.50],
            [2000,3430, 2.00, 27300,   6.50],
            [2500,3870, 1.90, 30500,   7.50],
            [3150,4600, 1.80, 36800,   7.50]
        ]
        self.puissance_dict = {
    "M110-23": {
        0.4: 0.08, 0.5: 0.12, 0.6: 0.16, 0.7: 0.21, 0.8: 0.26, 0.9: 0.32, 1.0: 0.39,
        1.1: 0.45, 1.2: 0.52, 1.3: 0.64, 1.35: 0.70, 1.4: 0.77, 1.45: 0.86, 1.5: 0.97,
        1.55: 1.16, 1.6: 1.37, 1.65: 1.56, 1.7: 2.26, 1.75: 4.16, 1.8: 7.80
    },
    "M120-27": {
        0.4: 0.08, 0.5: 0.12, 0.6: 0.17, 0.7: 0.22, 0.8: 0.28, 0.9: 0.34, 1.0: 0.41,
        1.1: 0.49, 1.2: 0.55, 1.3: 0.67, 1.35: 0.74, 1.4: 0.82, 1.45: 0.91, 1.5: 1.01,
        1.55: 1.17, 1.6: 1.37, 1.65: 1.72, 1.7: 2.56, 1.75: 4.36, 1.8: 7.01
    },
    "M130-30": {
        0.4: 0.09, 0.5: 0.14, 0.6: 0.19, 0.7: 0.24, 0.8: 0.30, 0.9: 0.37, 1.0: 0.44,
        1.1: 0.54, 1.2: 0.61, 1.3: 0.73, 1.35: 0.82, 1.4: 0.90, 1.45: 0.98, 1.5: 1.09,
        1.55: 1.23, 1.6: 1.43, 1.65: 1.70, 1.7: 2.70, 1.75: 4.32, 1.8: 6.17
    },
    "H75-23": {
        0.4: 0.082, 0.5: 0.117, 0.6: 0.157, 0.7: 0.201, 0.8: 0.255, 0.9: 0.323, 1.0: 0.398,
        1.1: 0.535, 1.2: 0.62, 1.3: 0.77, 1.35: 0.895, 1.4: 1.04, 1.45: 1.18, 1.5: 1.388,
        1.55: 1.55, 1.6: 1.723, 1.65: 1.925, 1.7: 2.50, 1.75: 2.58, 1.8: 3.77
    },
    "H80-23": {
        0.4: 0.07, 0.5: 0.11, 0.6: 0.14, 0.7: 0.19, 0.8: 0.23, 0.9: 0.29, 1.0: 0.35,
        1.1: 0.43, 1.2: 0.52, 1.3: 0.61, 1.35: 0.70, 1.4: 0.79, 1.45: 0.87, 1.5: 0.96,
        1.55: 1.08, 1.6: 1.21, 1.65: 1.32, 1.7: 1.68, 1.75: 2.0, 1.8: 2.72
    },
    "H85-23": {
        0.4: 0.069, 0.5: 0.101, 0.6: 0.137, 0.7: 0.176, 0.8: 0.202, 0.9: 0.268, 1.0: 0.342,
        1.1: 0.378, 1.2: 0.44, 1.3: 0.54, 1.35: 0.59, 1.4: 0.64, 1.45: 0.72, 1.5: 0.81,
        1.55: 0.93, 1.6: 1.07, 1.65: 1.18, 1.7: 1.46, 1.75: 1.7, 1.8: 1.717
    },
    "H95-27": {
        0.4: 0.077, 0.5: 0.112, 0.6: 0.152, 0.7: 0.206, 0.8: 0.245, 0.9: 0.298, 1.0: 0.37,
        1.1: 0.42, 1.2: 0.52, 1.3: 0.63, 1.35: 0.675, 1.4: 0.73, 1.45: 0.79, 1.5: 0.84,
        1.55: 0.91, 1.6: 0.994, 1.65: 1.134, 1.7: 1.36, 1.75: 1.49, 1.8: 2.568
    },
    "H105-30": {
        0.4: 0.08, 0.5: 0.12, 0.6: 0.17, 0.7: 0.22, 0.8: 0.27, 0.9: 0.33, 1.0: 0.41,
        1.1: 0.42, 1.2: 0.52, 1.3: 0.62, 1.35: 0.69, 1.4: 0.74, 1.45: 0.79, 1.5: 0.85,
        1.55: 0.92, 1.6: 1.01, 1.65: 1.11, 1.7: 1.38, 1.75: 1.47, 1.8: 1.89
    }
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
        courant_fprim = self.calculer_courant_phase_primaire()
        courant_fsec = self.calculer_courant_phase_secondaire()
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
            "CourantPhasePrim": courant_fprim,
            "CourantPhaseSec": courant_fsec,
            "ClasseTensionPrim": self.calculer_classe_tension_primaire(),
            "ClasseTensionSec": self.calculer_classe_tension_secondaire(),
            "classeTensionlast": self.calculer_rapport_transformation(),
            "pertes_cuivre_W": pertes_cuivre,
            "pertes_fer_W": pertes_fer,
        }

    def calculer_bobinage(self) -> Dict[str, Any]:
        tension_primaire = self.entrees["tension_primaire"]
        tension_secondaire = self.entrees["tension_secondaire"]

        spiresvsp = self.calculer_spires_vsp()
        nombre_spires_prim = self.calculer_nombre_spires_primaire()
        nombre_spires_sec = self.calculer_nombre_spires_secondaire()

        section_conducteur_prim = self.calculer_section_conducteur_primaire()
        section_conducteur_sec = self.calculer_section_conducteur_secondaire()

        return {
            "spiresVsp": spiresvsp,
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
            "echauffement1": round(temperature_max),
            "Classe thermique": self.obtenir_classe_thermique(temperature_max),
            "echauffement2": self.calculer_echauffement2(),
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
        return self.entrees["tension_primaire"] 

    def calculer_tension_phase_secondaire(self) -> float:
        if self.entrees["couplage_secondaire"] == "D" :
            return self.entrees["tension_secondaire"]
        if self.entrees["couplage_secondaire"] in ["Y","YN"]:
            return self.entrees["tension_secondaire"] / math.sqrt(3)
        if self.entrees["couplage_secondaire"] in ["Z","ZN"]:
            return self.entrees["tension_secondaire"] / 3/2

    def calculer_courant_ligne_primaire(self) -> float:
        return (self.entrees["puissance_kva"] * 1000) / (self.entrees["tension_primaire"] * math.sqrt(3))

    def calculer_courant_ligne_secondaire(self) -> float:
        return (self.entrees["puissance_kva"] * 1000) / (self.entrees["tension_secondaire"] * math.sqrt(3))
    def calculer_courant_phase_primaire(self) -> float :
        if self.entrees["couplage_primaire"] == "D" :
            return self.calculer_courant_ligne_primaire()/ math.sqrt(3)
        return self.calculer_courant_ligne_primaire()
    def calculer_courant_phase_secondaire(self) -> float :
        if self.entrees["couplage_secondaire"] == "D" :
            return self.calculer_courant_ligne_secondaire()/ math.sqrt(3)
        return self.calculer_courant_ligne_secondaire()

    def calculer_classe_tension_primaire(self) -> str:
        return self.obtenir_classe_tension(self.entrees["tension_primaire"])

    def calculer_classe_tension_secondaire(self) -> str:
        return self.obtenir_classe_tension(self.entrees["tension_secondaire"])
    def calculer_nombre_spires_primaire(self) -> int :
        return 0
    def calculer_rapport_transformation(self)-> float:
        if self.couplage in ["DYN11","YZN11","YND11"]:
            return self.entrees["tension_primaire"]/self.entrees["tension_secondaire"] * math.sqrt(3)
        if self.couplage in ["YNYN0","DD0"]:
            return self.entrees["tension_primaire"]/self.entrees["tension_secondaire"]
        return 0

    def calculer_nombre_spires_secondaire(self) -> int:
        rapport_spires = self.entrees["tension_primaire"] / self.entrees["tension_secondaire"]
        return round(self.calculer_nombre_spires_primaire() / rapport_spires)
    def calculer_spires_vsp(self) -> float:
        return self.calculer_courant_phase_secondaire() / self.entrees["sps_bt"]
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
        temp = 100 - self.entrees["temperature"]
        return temp

    def calculer_echauffement2(self) -> int:
        temp = self.calculer_temperature_max() + 5
        return temp

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
