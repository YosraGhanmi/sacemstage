# core/innovative_calculations.py

def calculate_co2_footprint(mass_cu_kg, mass_fe_kg):
    """
    Calcul de l’empreinte carbone (en kg CO₂) basée sur les masses de matériaux.
    """
    co2_per_kg_cu = 4.0   # kg CO₂ / kg de cuivre (valeur moyenne)
    co2_per_kg_fe = 2.1   # kg CO₂ / kg d'acier

    co2_cu = mass_cu_kg * co2_per_kg_cu
    co2_fe = mass_fe_kg * co2_per_kg_fe

    return {
        "CO2_cuivre_kg": round(co2_cu, 2),
        "CO2_fer_kg": round(co2_fe, 2),
        "CO2_total_kg": round(co2_cu + co2_fe, 2)
    }


def calculate_lifetime_cost(initial_cost, annual_losses_W, energy_price_eur_per_kWh=0.15, years=15):
    """
    Coût total sur le cycle de vie (initial + pertes en euros sur N années)
    """
    annual_loss_kWh = annual_losses_W * 8760 / 1000  # W → kWh/an
    energy_cost_total = annual_loss_kWh * energy_price_eur_per_kWh * years
    return round(initial_cost + energy_cost_total, 2)


def improved_efficiency(power_W, losses_total_W):
    """
    Calcul du rendement (%) basé sur les pertes totales et puissance utile.
    """
    efficiency = power_W / (power_W + losses_total_W)
    return round(efficiency * 100, 2)


def cooling_class_suggestion(temp_rise_C):
    """
    Suggestion de classe d’isolation thermique en fonction de ΔT
    """
    if temp_rise_C <= 55:
        return "Classe A"
    elif temp_rise_C <= 70:
        return "Classe B"
    elif temp_rise_C <= 90:
        return "Classe F"
    else:
        return "Classe H"
def current_density_check(current_A, section_mm2, max_density_A_per_mm2=4.5):
    """
    Vérifie si la densité de courant est acceptable.
    """
    if section_mm2 is None or section_mm2 == 0:
        print("ERROR: section_mm2 cannot be None or zero in current_density_check.")
        # Return a default/error dictionary instead of crashing or returning None
        return {"densité_A/mm²": float('inf'), "statut": "Erreur de calcul: section nulle"}

    try:
        density = current_A / section_mm2
        status = "OK" if density <= max_density_A_per_mm2 else "Trop élevée"
        return {"densité_A/mm²": round(density, 2), "statut": status}
    except Exception as e:
        print(f"ERROR: An unexpected error occurred in current_density_check: {e}")
        return {"densité_A/mm²": float('inf'), "statut": "Erreur inattendue"}
def material_utilization_rate(volume_material_m3, volume_available_m3):
    """
    Calcule le taux d'utilisation du matériau (cuivre ou fer).
    """
    rate = (volume_material_m3 / volume_available_m3) * 100
    return round(rate, 2)


def eco_efficiency_score(efficiency_pct, co2_total_kg):
    """
    Score d’éco-efficacité basé sur le rendement et les émissions CO2.
    Plus le score est élevé, meilleure est l’éco-conception.
    """
    score = (efficiency_pct / co2_total_kg) * 100
    return round(score, 2)


def cooling_method_suggestion(losses_W, power_kVA):
    """
    Suggestion du type de refroidissement selon les pertes et la puissance.
    """
    losses_ratio = losses_W / (power_kVA * 1000)
    if losses_ratio < 0.01:
        return "Refroidissement naturel (ONAN)"
    elif losses_ratio < 0.02:
        return "Refroidissement air forcé (ONAF)"
    else:
        return "Refroidissement huile forcée (OFAF)"


def optimization_alerts(efficiency_pct, co2_kg, density_A_mm2):
    """
    Fournit des alertes sur les points à optimiser.
    """
    alerts = []
    if efficiency_pct < 97.5:
        alerts.append("Améliorer le rendement (cibles ≥ 98%)")
    if co2_kg > 1500:
        alerts.append("Réduire l'empreinte carbone (cuivre/fer)")
    if density_A_mm2 > 4.5:
        alerts.append("Réduire la densité de courant pour éviter la surchauffe")
    return alerts if alerts else ["Conception optimisée"]
def innovation_decision_assistant(power_W, losses_W, mass_cu, mass_fe, current, section, volume_cu, vol_slot):
    co2 = calculate_co2_footprint(mass_cu, mass_fe)
    efficiency = improved_efficiency(power_W, losses_W)
    density_info = current_density_check(current, section)
    utilization = material_utilization_rate(volume_cu, vol_slot)
    eco_score = eco_efficiency_score(efficiency, co2['CO2_total_kg'])
    alerts = optimization_alerts(efficiency, co2['CO2_total_kg'], density_info['densité_A/mm²'])

    return {
        "rendement_%": efficiency,
        "co2_total_kg": co2['CO2_total_kg'],
        "densité_A/mm²": density_info['densité_A/mm²'],
        "utilisation_matériau_%": utilization,
        "score_éco": eco_score,
        "alertes": alerts
    }
def smart_material_optimization(power_kVA, voltage_V, frequency_Hz):
    """
    Optimisation intelligente des matériaux basée sur la puissance, tension et fréquence.
    Retourne des recommandations pour le noyau et les enroulements.
    """
    # Formule empirique pour la section du noyau (en cm²)
    core_section_cm2 = 1.1 * (power_kVA ** 0.5) / (voltage_V ** 0.2 * frequency_Hz ** 0.15)
    
    # Estimation du rapport cuivre/fer optimal
    cu_fe_ratio = 0.25 + 0.02 * (power_kVA ** 0.33)
    
    return {
        "section_noyau_cm2": round(core_section_cm2, 2),
        "rapport_cuivre_fer": round(cu_fe_ratio, 3),
        "recommandation": "Utiliser des tôles à grains orientés pour >100kVA" if power_kVA > 100 else "Tôles standard suffisantes"
    }

def ai_loss_prediction(power_kVA, cooling_type, material_class):
    """
    Prédiction des pertes basée sur des modèles empiriques avancés.
    """
    # Coefficients basés sur l'analyse de données historiques
    base_losses = {
        "ONAN": 0.015 * power_kVA,
        "ONAF": 0.012 * power_kVA,
        "OFAF": 0.010 * power_kVA
    }
    
    material_factor = {
        "A": 1.0, "B": 0.95, "F": 0.9, "H": 0.85
    }
    
    predicted_losses = base_losses.get(cooling_type, 0.015 * power_kVA) * material_factor.get(material_class, 1.0)
    
    return round(predicted_losses, 2)

def dynamic_thermal_model(losses_W, cooling_method, ambient_temp_C=25):
    """
    Modèle thermique dynamique simplifié pour estimer la température de fonctionnement.
    """
    cooling_coefficients = {
        "ONAN": 0.05,
        "ONAF": 0.035,
        "OFAF": 0.02
    }
    
    temp_rise = losses_W * cooling_coefficients.get(cooling_method, 0.05)
    operating_temp = ambient_temp_C + temp_rise
    
    return {
        "élévation_temp_C": round(temp_rise, 1),
        "temp_fonctionnement_C": round(operating_temp, 1),
        "classe_thermique": cooling_class_suggestion(temp_rise)
    }

def circular_economy_score(mass_cu_kg, mass_fe_kg, recyclability_cu=0.95, recyclability_fe=0.85):
    """
    Score d'économie circulaire basé sur la recyclabilité des matériaux.
    """
    total_mass = mass_cu_kg + mass_fe_kg
    ce_score = (mass_cu_kg*recyclability_cu + mass_fe_kg*recyclability_fe) / total_mass * 100
    
    return {
        "score_économie_circulaire": round(ce_score, 1),
        "niveau": "Excellent" if ce_score >= 90 else "Bon" if ce_score >= 75 else "Moyen"
    }

def resonant_frequency_calculator(inductance_H, capacitance_F):
    """
    Calcule la fréquence de résonance pour éviter les problèmes de résonance.
    """
    from math import pi, sqrt
    fr = 1 / (2 * pi * sqrt(inductance_H * capacitance_F))
    return round(fr, 2)

def smart_cooling_optimization(losses_W, power_kVA, ambient_temp_C):
    """
    Optimisation intelligente du refroidissement avec prise en compte de la température ambiante.
    """
    loss_ratio = losses_W / (power_kVA * 1000)
    temp_factor = max(1, ambient_temp_C / 25)
    
    if loss_ratio * temp_factor < 0.008:
        return "ONAN (Naturel)"
    elif loss_ratio * temp_factor < 0.015:
        return "ONAF (Air forcé)"
    else:
        return "OFAF (Huile forcée) + Ventilation intelligente"

def transformer_aging_model(operating_temp_C, years, ref_temp_C=110):
    """
    Modèle de vieillissement du transformateur basé sur la température.
    """
    # Loi d'Arrhenius modifiée
    aging_rate = 2 ** ((operating_temp_C - ref_temp_C) / 6)
    equivalent_aging = years * aging_rate
    
    remaining_life_years = max(0, 30 - equivalent_aging)
    
    return {
        "taux_vieillissement": round(aging_rate, 2),
        "vie_équivalente_ans": round(equivalent_aging, 1),
        "vie_restante_estimée": round(remaining_life_years, 1)
    }

def harmonic_impact_analysis(thd_percent, frequency_Hz):
    """
    Analyse l'impact des harmoniques sur les pertes et le vieillissement.
    """
    harmonic_factor = 1 + 0.01 * (thd_percent ** 1.5)
    
    if frequency_Hz < 55 or frequency_Hz > 65:
        harmonic_factor *= 1.2
    
    return {
        "facteur_harmonique": round(harmonic_factor, 3),
        "impact": "Modéré" if harmonic_factor < 1.2 else "Élevé" if harmonic_factor < 1.5 else "Critique"
    }

def augmented_design_assistant(input_parameters):
    """
    Assistant de conception augmenté qui intègre toutes les méthodes innovantes.
    """
    # Extraction des paramètres d'entrée (exemple)
    power_kVA = input_parameters.get('power_kVA', 100)
    voltage_V = input_parameters.get('voltage_V', 1000)
    frequency_Hz = input_parameters.get('frequency_Hz', 50)
    ambient_temp = input_parameters.get('ambient_temp', 25)
    
    # Calculs intelligents
    material_opt = smart_material_optimization(power_kVA, voltage_V, frequency_Hz)
    predicted_losses = ai_loss_prediction(power_kVA, "ONAN", "A")
    cooling_opt = smart_cooling_optimization(predicted_losses*1000, power_kVA, ambient_temp)
    thermal_model = dynamic_thermal_model(predicted_losses*1000, cooling_opt, ambient_temp)
    
    return {
        "optimisation_matières": material_opt,
        "prédiction_pertes_W": predicted_losses,
        "refroidissement_optimal": cooling_opt,
        "modèle_thermique": thermal_model,
        "recommandations": [
            "Considérer des conducteurs à haute conductivité pour >500kVA",
            "Optimiser la forme du noyau pour réduire les pertes fer",
            "Prévoir des capteurs IoT pour le monitoring en temps réel"
        ]
    }

def quantum_efficiency_estimator(power_W, losses_W, quantum_factor=0.98):
    """
    Estimation de l'efficacité quantique théorique en considérant des matériaux avancés.
    """
    classical_eff = improved_efficiency(power_W, losses_W)
    quantum_eff = min(100, classical_eff * (1 + (1 - classical_eff/100) * quantum_factor))
    
    return {
        "rendement_classique_%": classical_eff,
        "rendement_quantique_estimé_%": round(quantum_eff, 2),
        "gain_potentiel": round(quantum_eff - classical_eff, 2)
    }
