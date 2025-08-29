from dataclasses import dataclass
from typing import Optional
import math


@dataclass
class CoreGeometry:
    """
    Dimensions géométriques du noyau du transformateur.

    Attributes:
        core_type: Type de noyau ('EI', 'UI', 'Tore', etc.).
        leg_width_mm: Largeur de la jambe centrale (mm).
        yoke_height_mm: Hauteur du yoke (mm).
        window_width_mm: Largeur de la fenêtre de bobinage (mm).
        window_height_mm: Hauteur de la fenêtre de bobinage (mm).
        stacking_factor: Facteur d'empilement du noyau (entre 0 et 1).
    """
    core_type: str
    leg_width_mm: float
    yoke_height_mm: float
    window_width_mm: float
    window_height_mm: float
    stacking_factor: float = 0.95

    def core_area_mm2(self) -> float:
        """Surface effective du noyau (mm²)."""
        return self.leg_width_mm * self.yoke_height_mm * self.stacking_factor

    def window_area_mm2(self) -> float:
        """Surface de la fenêtre de bobinage (mm²)."""
        return self.window_width_mm * self.window_height_mm


@dataclass
class TankGeometry:
    """
    Dimensions géométriques du réservoir.

    Attributes:
        tank_type: Type de réservoir ('cylindrique' ou 'rectangulaire').
        length_mm: Longueur du réservoir (mm).
        width_mm: Largeur ou diamètre du réservoir (mm).
        height_mm: Hauteur du réservoir (mm).
        thickness_mm: Épaisseur des parois (mm).
    """
    tank_type: str
    length_mm: float
    width_mm: float
    height_mm: float
    thickness_mm: float = 5.0

    def volume_liters(self) -> float:
        """Volume intérieur du réservoir en litres."""
        if self.tank_type == "cylindrique":
            radius_m = (self.width_mm / 2) / 1000
            height_m = self.height_mm / 1000
            return math.pi * radius_m ** 2 * height_m * 1000  # m³ → litres

        if self.tank_type == "rectangulaire":
            volume_m3 = (
                (self.length_mm / 1000)
                * (self.width_mm / 1000)
                * (self.height_mm / 1000)
            )
            return volume_m3 * 1000

        raise ValueError(f"Type de réservoir non reconnu: {self.tank_type}")

    def surface_area_mm2(self) -> float:
        """Surface extérieure du réservoir (mm²)."""
        if self.tank_type == "cylindrique":
            radius_mm = self.width_mm / 2
            return (
                2 * math.pi * radius_mm * (radius_mm + self.height_mm)
            )

        if self.tank_type == "rectangulaire":
            return 2 * (
                self.length_mm * self.width_mm
                + self.length_mm * self.height_mm
                + self.width_mm * self.height_mm
            )

        raise ValueError(f"Type de réservoir non reconnu: {self.tank_type}")


def get_standard_core_dimensions(
    core_type: str, power_kva: float
) -> CoreGeometry:
    """
    Fournit des dimensions approximatives du noyau selon le type et la puissance.

    Args:
        core_type: 'EI' ou autre type de noyau.
        power_kva: Puissance apparente en kVA.

    Returns:
        Instance de CoreGeometry.
    """
    # Paramètres de base (à ajuster selon normes ou tables constructeur)
    if core_type.upper() == "EI":
        leg_width = 20 + 2 * power_kva
        yoke_height = 25 + 1.5 * power_kva
        window_width = 30 + 3 * power_kva
        window_height = 40 + 2 * power_kva
    else:
        leg_width = 25 + 2.2 * power_kva
        yoke_height = 30 + 1.6 * power_kva
        window_width = 35 + 2.8 * power_kva
        window_height = 45 + 2.1 * power_kva

    return CoreGeometry(
        core_type=core_type,
        leg_width_mm=leg_width,
        yoke_height_mm=yoke_height,
        window_width_mm=window_width,
        window_height_mm=window_height
    )
