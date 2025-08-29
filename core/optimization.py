# core/optimization.py
import random
import numpy as np
from scipy.optimize import minimize
from core import thermal
# ---- FONCTIONS D’ÉVALUATION ----


def generate_real_variants(base_inputs, param_to_vary, variation_range, num_variants=5):
    from core.calculation_pipeline import calculate_all
    variants = []
    
    for i in range(num_variants):
        new_inputs = base_inputs.copy()

        if param_to_vary == "b_max":
            new_inputs["b_max"] = round(base_inputs["b_max"] * (1 + variation_range * (i - num_variants//2) / num_variants), 3)

        try:
            result = calculate_all(new_inputs)

            variant = {
                "nom": f"Variante {i+1}",
                "rendement": result.get("improved_efficiency_percent"),
                "poids": result.get("copper_mass_kg"),
                "coût": result.get("lifetime_cost_eur"),
                "pertes": result.get("thermal", {}).get("losses_total_W"),
                "details": result
            }

            variants.append(variant)

        except Exception as e:
            print(f"⚠️ Erreur sur la variante {i+1} : {e}")

    return variants

def generate_design_variants(base_design, criteria, num_variants=10):
    variants = []
    for i in range(num_variants):
        variant = base_design.copy()
        if "Coût" in criteria:
            variant["coût"] = round(base_design["coût"] * random.uniform(0.9, 1.1), 2)
        if "Rendement" in criteria:
            variant["rendement"] = round(base_design["rendement"] * random.uniform(0.98, 1.02), 4)
        if "Poids" in criteria:
            variant["poids"] = round(base_design["poids"] * random.uniform(0.85, 1.15), 1)
        if "Pertes" in criteria:
            variant["pertes"] = round(base_design["pertes"] * random.uniform(0.9, 1.1), 2)
        variant["nom"] = f"Variante {i+1}"
        variants.append(variant)
    return variants


def compute_masse(params):
    s_fer, s_cuivre = params
    densite_fer = 7.6  # g/cm³
    densite_cuivre = 8.9  # g/cm³
    masse_fer = s_fer * 30 * densite_fer  # profondeur fixe = 30 cm
    masse_cuivre = s_cuivre * 2 * densite_cuivre  # longueur fil estimée = 2 m
    return masse_fer + masse_cuivre  # en g

def compute_cout(params):
    s_fer, s_cuivre = params
    prix_fer = 2.0  # €/kg
    prix_cuivre = 8.0  # €/kg
    masse_fer = compute_masse([s_fer, 0]) / 1000  # kg
    masse_cuivre = compute_masse([0, s_cuivre]) / 1000
    return masse_fer * prix_fer + masse_cuivre * prix_cuivre

def compute_rendement(params, voltage, power):
    pertes = compute_total_losses(params, voltage, power)
    rendement = power / (power + pertes)
    return rendement


def compute_total_losses(params, voltage, power):
    s_fer, s_cuivre = params
    pertes_fer = 1.2 * s_fer**1.5  # pertes à vide
    pertes_cuivre = 0.008 * power**2 / s_cuivre  # pertes Joules
    return pertes_fer + pertes_cuivre

def temperature_constraint(params):
    s_fer, s_cuivre = params
    température = 20 + 0.03 * (s_fer + s_cuivre)**1.2
    return 90 - température


# ---- OBJECTIF PONDÉRÉ ----

def multi_objective_cost(params, voltage, power, weights):
    """
    Fonction pondérée :
    - weights = (w_masse, w_cout, w_rendement)
    - rendement est inversé car on cherche à le maximiser
    """
    w_masse, w_cout, w_rdt = weights
    masse = compute_masse(params) / 1000  # kg
    cout = compute_cout(params)
    rendement = compute_rendement(params, voltage, power)

    return w_masse * masse + w_cout * cout + w_rdt * (1 - rendement)


# ---- OPTIMISATION ----

def optimize_transformer_multi(voltage, power, weights=(0.4, 0.4, 0.2)):
    bounds = [(10, 200), (50, 1000)]  # (s_fer, s_cuivre)
    initial_guess = [60, 200]
    constraints = [{'type': 'ineq', 'fun': temperature_constraint}]

    result = minimize(
        multi_objective_cost,
        initial_guess,
        args=(voltage, power, weights),
        bounds=bounds,
        constraints=constraints,
        method='SLSQP'
    )

    if result.success:
        s_fer_opt, s_cuivre_opt = result.x
        losses = compute_total_losses(result.x, voltage, power)
        masse = compute_masse(result.x) / 1000
        cout = compute_cout(result.x)
        rendement = compute_rendement(result.x, voltage, power)
        temp = 20 + 0.03 * (s_fer_opt + s_cuivre_opt)**1.2

        return {
            "section_fer_cm2": round(s_fer_opt, 2),
            "section_cuivre_mm2": round(s_cuivre_opt, 2),
            "pertes_totales_W": round(losses, 2),
            "rendement": round(rendement * 100, 2),
            "masse_kg": round(masse, 2),
            "coût_€": round(cout, 2),
            "température_maximale_C": round(temp, 2),
        }
    else:
        raise ValueError("Échec de l'optimisation : " + result.message)
