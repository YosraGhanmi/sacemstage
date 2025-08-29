import math
from typing import Tuple

STEEL_DENSITY_KG_PER_M3 = 7850  # Densité moyenne de l'acier (kg/m³)
PAINT_COVERAGE_M2_PER_LITER = 10  # m² de surface couverte par litre de peinture
PAINT_SAFETY_FACTOR = 1.2  # Surépaisseur pour retouches et double couche

def calculate_tank_dimensions(core_height_m: float, core_diameter_m: float, margin_m: float = 0.1) -> Tuple[float, float, float]:
    """
    Calcule les dimensions du réservoir (interne + marges + espace huile).

    On ajoute 100 mm d'espace minimum autour du noyau, ajustable par 'margin_m'.
    """
    height = core_height_m + 2 * margin_m + 0.2  # 0.2 m pour l'espace huile supérieur/inferieur
    width = core_diameter_m + 2 * margin_m
    depth = core_diameter_m + 2 * margin_m
    return height, width, depth

def calculate_tank_surface_m2(height_m: float, width_m: float, depth_m: float) -> float:
    """
    Surface externe du réservoir (inclut toit et fond).
    """
    side_area = 2 * (height_m * width_m + height_m * depth_m + width_m * depth_m)
    return side_area

def calculate_tank_thickness_m(height_m: float, width_m: float, depth_m: float) -> float:
    """
    Épaisseur des parois en m selon les dimensions (plus grand => plus épais).
    """
    max_dim = max(height_m, width_m, depth_m)
    if max_dim < 1.2:
        return 0.006  # 6 mm
    elif max_dim < 2.0:
        return 0.008  # 8 mm
    else:
        return 0.010  # 10 mm

def calculate_tank_mass_kg(height_m: float, width_m: float, depth_m: float) -> float:
    """
    Masse estimée du réservoir acier (parois + toit + fond + renforts).
    """
    thickness_m = calculate_tank_thickness_m(height_m, width_m, depth_m)
    surface_m2 = calculate_tank_surface_m2(height_m, width_m, depth_m)
    volume_steel_m3 = surface_m2 * thickness_m

    basic_mass = volume_steel_m3 * STEEL_DENSITY_KG_PER_M3

    # On ajoute 10% pour les soudures, renforts, brides, etc.
    return basic_mass * 1.1

def calculate_paint_required_liters(surface_m2: float, coverage_m2_per_l: float = PAINT_COVERAGE_M2_PER_LITER) -> float:
    """
    Quantité de peinture nécessaire pour couvrir la surface, avec marge.
    """
    return (surface_m2 * PAINT_SAFETY_FACTOR) / coverage_m2_per_l

def estimate_accessory_mass_kg(tank_mass_kg: float) -> float:
    """
    Estime la masse des accessoires (prises, boîtiers, etc.) en fonction de la masse du réservoir.

    Args:
        tank_mass_kg: Masse du réservoir en acier (kg)

    Returns:
        Masse estimée des accessoires (kg)
    """
    if tank_mass_kg < 300:
        return 30.0
    elif tank_mass_kg < 800:
        return 60.0
    else:
        return 100.0


def calculate_total_mechanical_mass_kg(tank_mass_kg: float, accessory_mass_kg: float) -> float:
    """
    Masse totale de la structure mécanique : réservoir + accessoires.
    """
    return tank_mass_kg + accessory_mass_kg

def calculate_mechanical_block(core_height_m: float, core_diameter_m: float) -> dict:
    h, w, d = calculate_tank_dimensions(core_height_m, core_diameter_m)
    surface = calculate_tank_surface_m2(h, w, d)
    thickness = calculate_tank_thickness_m(h, w, d)
    tank_mass = calculate_tank_mass_kg(h, w, d)
    
    # ✅ Vérifiez bien que ceci est présent et correctement écrit
    accessory_mass = estimate_accessory_mass_kg(tank_mass)
    
    total_mass = calculate_total_mechanical_mass_kg(tank_mass, accessory_mass)
    paint_liters = calculate_paint_required_liters(surface)
    oil_volume_liters = calculate_oil_volume_liters(h, w, d, thickness)

    return {
        "height_m": h,
        "width_m": w,
        "depth_m": d,
        "surface_m2": surface,
        "tank_thickness_m": thickness,
        "tank_mass_kg": round(tank_mass, 2),
        "accessory_mass_kg": round(accessory_mass, 2),
        "total_mechanical_mass_kg": round(total_mass, 2),
        "paint_required_liters": round(paint_liters, 2),
        "oil_volume_liters": oil_volume_liters
    }

def calculate_oil_volume_liters(
    height_m: float,
    width_m: float,
    depth_m: float,
    thickness_m: float = 0.006,
    fill_ratio: float = 0.9
) -> float:
    """
    Calcule le volume d’huile à l’intérieur du réservoir (en litres).

    - fill_ratio: ratio de remplissage utile (souvent 90 %).
    - thickness_m: épaisseur des parois.
    """
    internal_height = height_m - 2 * thickness_m
    internal_width = width_m - 2 * thickness_m
    internal_depth = depth_m - 2 * thickness_m

    internal_volume_m3 = internal_height * internal_width * internal_depth
    oil_volume_m3 = internal_volume_m3 * fill_ratio

    return round(oil_volume_m3 * 1000, 2)  # En litres
