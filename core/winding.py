# core/winding.py
from core.electrical import calculate_electrical_params, calcul_tension_1_phase, calcul_tension_2_phase

import math

def compute_number_of_turns(voltage, freq, B_max, Ae_m2):
    return voltage / (4.44 * freq * B_max * Ae_m2)

def compute_conductor_section(current, J=3):
    return current / J  # mm²

def compute_conductor_length(n_turns, avg_perimeter_m):
    return n_turns * avg_perimeter_m

def compute_resistance(rho, length_m, section_mm2):
    section_m2 = section_mm2 * 1e-6
    return rho * length_m / section_m2

def compute_copper_losses(current, resistance):
    return current**2 * resistance

def compute_copper_mass(length_m, section_mm2, density=8900):
    volume_m3 = length_m * section_mm2 * 1e-6
    return volume_m3 * density

##### Primary Calcule#####
def calculer_courant_bt(puissance_kVA, tension_BT):
    return (puissance_kVA * 1000) / (math.sqrt(3) * tension_BT)

def calculer_courant_ht(S_kVA, V_V, transformer_type):
    """
    Calcule le courant électrique d’un transformateur monophasé ou triphasé.

    :param S_kVA: Puissance apparente en kVA
    :param V_V: Tension en volts
    :param transformer_type: Type de transformateur ("Monophasé" ou "Triphasé")
    :return: Courant en ampères (A)
    """
    S_VA = S_kVA * 1000
    if transformer_type == "Triphasé":
        I = S_VA / (math.sqrt(3) * V_V)
    elif transformer_type == "Monophasé":
        I = S_VA / V_V
    else:
        raise ValueError("Le type de transformateur doit être 'Monophasé' ou 'Triphasé'.")
    return round(I, 2)

def calculer_nbre_spires_BT(nb_sps_MT_max, tension_BT, tension_MT):
    return round((nb_sps_MT_max * tension_BT) / tension_MT)

def calculer_epaisseur_spire_BT(section_cond_mm2, hauteur_cond_mm):
    return section_cond_mm2 / hauteur_cond_mm

def calculer_epaisseur_isolement(nb_papier, ep_papier_mm, iso_couche_BT):
    return nb_papier * ep_papier_mm + iso_couche_BT

def calculer_epaisseur_bobine_BT(nbcouches_BT, epaisseur_spire_BT, epaisseur_isolement, nb_canaux_BT, largeur_canal_BT):
    return nbcouches_BT * (epaisseur_spire_BT + epaisseur_isolement) + (nb_canaux_BT * largeur_canal_BT)

def calculer_dim_ext_BT(dim_int_BT, epaisseur_bobine_BT):
    return dim_int_BT + 2 * epaisseur_bobine_BT

def calculer_hauteur_bobine_BT(nbre_spires_BT, nbcouches_BT, hauteur_cond_mm, hauteur_collier):
    return math.ceil(nbre_spires_BT / nbcouches_BT) * hauteur_cond_mm + 2 * hauteur_collier

def calculer_contours(dim_int_BT, dim_ext_BT):
    contour_int = math.pi * dim_int_BT
    contour_ext = math.pi * dim_ext_BT
    contour_moy = math.pi * ((dim_int_BT + dim_ext_BT) / 2)
    return contour_int, contour_ext, contour_moy

def calculer_longueur_spire_mm(dim_int_BT, epaisseur_BT):
    return math.pi * (dim_int_BT + epaisseur_BT)

def calculer_nb_spires_total(nbcouches_BT, spires_max_par_couche):
    return nbcouches_BT * spires_max_par_couche

def calculer_longueur_totale_fil_m(longueur_spire_mm, nb_spires_tot):
    return (longueur_spire_mm * nb_spires_tot) / 1000

def calculer_volume_cuivre_cm3(longueur_totale_fil_m, section_cond_mm2):
    return longueur_totale_fil_m * section_cond_mm2 * 0.01  # conversion mm² * m → cm³

def calculer_masse_cuivre_kg(volume_cuivre_cm3, densite_cuivre=8.96):
    return volume_cuivre_cm3 * densite_cuivre / 1000  # conversion cm³ → kg

def calculer_nb_sps_MT_max(tension_MT, spires_par_volt=0.8):
    return round(tension_MT * spires_par_volt)

def calucler_vsp(f, b_max):
    return (2 * 3.14 * f * 168990) * b_max / (1.411 * 1000000)

def nb_sps_BT(tension_phase_2, vsp):
    return tension_phase_2 / vsp

def vsp_usine(tension_phase_2, sps_bt_def):
    return tension_phase_2 / sps_bt_def

def bmax_calc(vsp_sacem, f):
    return (vsp_sacem * 1.414 * 1000000) / (2 * 3.1415 * f * 1689)

def nb_sps_mt(tension, vsp_usine):
    return tension / vsp_usine

def nb_sps_max(sps_mt, reglage):
    return sps_mt * (100 + reglage) / 100

def rapport_transformation(nb_sps_mt, bt_def):
    return nb_sps_mt / bt_def

def rapport_tensions(tension, u2_phase):
    return tension / u2_phase

#### Bobinage secondaire ######

def Poids_bobinage_effectif(winding_material):
    if winding_material == "Cuivre":
        return 8.9
    else:
        return 2.7

def coeficient_pertes(winding_material):
    if winding_material == "Cuivre":
        return 2.286
    else:
        return 12.18

def coeficient_section(cooling_bob_type):
    if cooling_bob_type == "Meplat":
        return 0.89
    else:
        return 1

def isolation_axial(cooling_bob_type):
    if cooling_bob_type == "Meplat":
        return 0.65
    else:
        return 0

def isolation_radiale(cooling_bob_type):
    if cooling_bob_type == "Meplat":
        return 0.5
    else:
        return 0

def section_cond_BT(Hauteur, Epaisseur, Etage, Nombre_cond):
    return Hauteur * Epaisseur * Etage * Nombre_cond

def calcule_J_BT(U2_phase, section_cond_Bt):
    return U2_phase / section_cond_Bt

def spires_max_Bt(sps_bt, Couche_bt):
    return sps_bt / Couche_bt

def calcule_epaisseur_bt(isol_radial, Etage, cooling_bob_type, Epaisseur, cond, couche_bt, largeur_canal_BT, isolement, Nb_canaux_bt):
    if cooling_bob_type == "Bande":
        return Epaisseur * cond * couche_bt + (couche_bt - 1) * isolement + Nb_canaux_bt * largeur_canal_BT
    else:
        return (Epaisseur + isol_radial) * Etage * couche_bt + (couche_bt - 1) * isolement * Nb_canaux_bt * largeur_canal_BT

def calcule_dim_int_BT(depart, dis_circuit_bt):
    return depart + 2 * dis_circuit_bt
