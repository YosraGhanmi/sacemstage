import math
from typing import Tuple

# --- Constantes physiques pour l'air à 300 K ---
AIR_THERMAL_CONDUCTIVITY = 0.0262    # W/m·K
AIR_PRANDTL_NUMBER = 0.71            # sans dimension
AIR_KINEMATIC_VISCOSITY = 1.846e-5   # m²/s
AIR_THERMAL_EXPANSION = 1 / 300.0    # 1/K
GRAVITY = 9.81                       # m/s²
STEFAN_BOLTZMANN = 5.67e-8           # W/m²·K⁴ (constante de Stefan-Boltzmann)

# --- Fonctions existantes conservées ---
def total_losses(p_cu_w: float, p_fe_w: float) -> float:
    return p_cu_w + p_fe_w

def calculate_temperature_rise(losses_w: float, thermal_resistance_c_per_w: float) -> float:
    return losses_w * thermal_resistance_c_per_w

def calculate_final_temperature(ambient_temp_c: float, temp_rise_c: float) -> float:
    return ambient_temp_c + temp_rise_c

def calculate_required_surface(losses_w: float, allowable_temp_rise_c: float, coeff: float = 5.0) -> float:
    if allowable_temp_rise_c <= 0:
        raise ValueError("L'élévation de température doit être > 0")
    return (losses_w * coeff) / allowable_temp_rise_c

def cooling_class_check(temp_rise_c: float, cooling_class: str = "A") -> bool:
    class_limits = {"A": 60, "B": 80, "F": 100, "H": 125}
    return temp_rise_c <= class_limits.get(cooling_class.upper(), 60)

# --- Convection naturelle (inchangé) ---
def calculate_grashof_number(delta_t_c: float, char_length_m: float) -> float:
    return (GRAVITY * AIR_THERMAL_EXPANSION * delta_t_c * char_length_m**3) / (AIR_KINEMATIC_VISCOSITY**2)

def calculate_rayleigh_number(delta_t_c: float, char_length_m: float) -> float:
    return calculate_grashof_number(delta_t_c, char_length_m) * AIR_PRANDTL_NUMBER

def calculate_nusselt_number_vertical(rayleigh: float) -> float:
    if rayleigh < 1e4:
        return 0.0
    elif rayleigh < 1e9:
        return 0.59 * rayleigh**0.25
    else:
        return 0.1 * rayleigh**(1/3)

def calculate_convection_coefficient(nusselt: float, char_length_m: float) -> float:
    return nusselt * AIR_THERMAL_CONDUCTIVITY / char_length_m

def calculate_temp_rise_convection(losses_w: float, surface_m2: float, char_length_m: float,
                                   max_iterations: int = 10, tol: float = 0.1) -> float:
    delta_t = 10.0
    for _ in range(max_iterations):
        ra = calculate_rayleigh_number(delta_t, char_length_m)
        nu = calculate_nusselt_number_vertical(ra)
        h = calculate_convection_coefficient(nu, char_length_m)
        if h == 0:
            return float('inf')
        new_delta_t = losses_w / (h * surface_m2)
        if abs(new_delta_t - delta_t) < tol:
            return new_delta_t
        delta_t = new_delta_t
    return delta_t

# --- ✅ Nouveautés innovantes --- 

def calculate_radiation_loss(temp_surface_c: float, temp_ambient_c: float, emissivity: float, surface_m2: float) -> float:
    """Pertes par rayonnement (W)."""
    t_s = temp_surface_c + 273.15
    t_a = temp_ambient_c + 273.15
    return emissivity * STEFAN_BOLTZMANN * surface_m2 * (t_s**4 - t_a**4)

def calculate_forced_convection_coefficient(air_velocity_m_s: float) -> float:
    """Estimation simplifiée de h forcé en air (dépend de la vitesse)."""
    return 10.45 - air_velocity_m_s + 10 * math.sqrt(air_velocity_m_s)

def calculate_combined_temp_rise(losses_w: float, surface_m2: float, temp_ambient_c: float,
                                 char_length_m: float, emissivity: float = 0.9) -> float:
    """
    Élévation de température par convection + rayonnement combinés (formule de Newton généralisée).
    """
    delta_t = 10.0
    for _ in range(10):
        rayleigh = calculate_rayleigh_number(delta_t, char_length_m)
        nu = calculate_nusselt_number_vertical(rayleigh)
        h_conv = calculate_convection_coefficient(nu, char_length_m)
        rad_loss = calculate_radiation_loss(temp_ambient_c + delta_t, temp_ambient_c, emissivity, surface_m2)
        conv_loss = h_conv * surface_m2 * delta_t
        total_dissipation = conv_loss + rad_loss
        new_delta_t = losses_w / (total_dissipation / delta_t)
        if abs(new_delta_t - delta_t) < 0.1:
            return new_delta_t
        delta_t = new_delta_t
    return delta_t

def estimate_thermal_time_constant(mass_kg: float, specific_heat_j_kgk: float, h_total: float, surface_m2: float) -> float:
    """Constante de temps thermique (s)."""
    return (mass_kg * specific_heat_j_kgk) / (h_total * surface_m2)

def estimate_thermal_response(temp_final: float, temp_init: float, time_s: float, time_constant_s: float) -> float:
    """Température à un instant donné dans le régime transitoire."""
    return temp_final - (temp_final - temp_init) * math.exp(-time_s / time_constant_s)

def calculate_thermal_efficiency(power_input_w: float, losses_w: float) -> float:
    """Rendement thermique simplifié."""
    return (power_input_w - losses_w) / power_input_w if power_input_w > 0 else 0.0
def calculate_oil_temp_rise_ONAN(losses_w: float, oil_mass_kg: float, oil_specific_heat: float,
                                 surface_m2: float, ambient_temp_c: float,
                                 oil_to_wall_coeff: float = 100.0,  # h_int W/m²·K
                                 wall_to_air_coeff: float = 10.0    # h_ext W/m²·K
                                 ) -> float:
    """
    Calcule l'élévation de température pour un transformateur ONAN (refroidi à l’huile, naturel).
    Approche par résistance thermique équivalente série.
    """
    h_eq = 1 / ((1 / oil_to_wall_coeff) + (1 / wall_to_air_coeff))  # Résistance série
    delta_t = losses_w / (h_eq * surface_m2)
    return delta_t


def calculate_oil_temp_rise_ONAF(losses_w: float, oil_mass_kg: float, oil_specific_heat: float,
                                 surface_m2: float, ambient_temp_c: float,
                                 air_velocity_m_s: float = 3.0,
                                 oil_to_wall_coeff: float = 100.0
                                 ) -> float:
    """
    Élément de calcul pour un transformateur ONAF (ventilateurs côté air).
    Augmentation du h_ext par convection forcée.
    """
    h_ext_forced = calculate_forced_convection_coefficient(air_velocity_m_s)  # dépend de la vitesse de l'air
    h_eq = 1 / ((1 / oil_to_wall_coeff) + (1 / h_ext_forced))
    delta_t = losses_w / (h_eq * surface_m2)
    return delta_t


def estimate_hotspot_temperature_ONAN(ambient_temp_c: float, delta_t_top_oil: float,
                                      delta_t_hotspot: float = 15.0) -> float:
    """Estimation de la température du point chaud (hotspot) en ONAN."""
    return ambient_temp_c + delta_t_top_oil + delta_t_hotspot


def estimate_oil_flow_velocity(losses_w: float, oil_density: float = 870.0, pipe_section_m2: float = 0.01,
                               g: float = 9.81, height_m: float = 1.5, delta_temp_c: float = 10.0) -> float:
    """
    Estime la vitesse d'écoulement naturel de l’huile par poussée d’Archimède.
    Simplifié (utilisé pour valider si besoin de ONAF).
    """
    expansion = 0.0007  # Coefficient d’expansion thermique de l’huile
    force = oil_density * g * height_m * expansion * delta_temp_c
    acceleration = force / oil_density
    return (2 * acceleration * height_m)**0.5  # v = sqrt(2aH)
