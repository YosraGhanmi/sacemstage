# core/calculation_pipeline.py

from core.electrical import calculate_electrical_params, calcul_tension_1_phase, calcul_tension_2_phase
from core.geometry import get_standard_core_dimensions, TankGeometry
from core.mechanical import (
    calculate_tank_surface_m2,
    calculate_tank_mass_kg,
    calculate_paint_required_liters,
    calculate_total_mechanical_mass_kg,
    estimate_accessory_mass_kg
)
from core.innovative_calculations import (
    calculate_co2_footprint,
    calculate_lifetime_cost,
    improved_efficiency,
    cooling_class_suggestion,
    innovation_decision_assistant
)
from core.thermal import (
    total_losses,
    calculate_temp_rise_convection,
    calculate_final_temperature,
    cooling_class_check, calculate_combined_temp_rise, calculate_convection_coefficient, calculate_forced_convection_coefficient, calculate_grashof_number, calculate_nusselt_number_vertical,
    calculate_oil_temp_rise_ONAF, calculate_oil_temp_rise_ONAN, calculate_radiation_loss, calculate_rayleigh_number, calculate_required_surface, calculate_temperature_rise,
    calculate_thermal_efficiency, estimate_thermal_time_constant, estimate_hotspot_temperature_ONAN
    
)
from core.winding import (
    compute_number_of_turns,
    compute_conductor_section,
    compute_conductor_length,
    compute_resistance,
    compute_copper_losses,
    compute_copper_mass,
    calculer_courant_bt,
    calculer_nbre_spires_BT,
    calculer_courant_ht,
    calculer_epaisseur_spire_BT,
    calculer_epaisseur_isolement,
    calculer_epaisseur_bobine_BT,
    calculer_dim_ext_BT,
    calculer_hauteur_bobine_BT,
    calculer_contours,
    calculer_longueur_spire_mm,
    calculer_nb_spires_total,
    calculer_longueur_totale_fil_m,
    calculer_volume_cuivre_cm3,
    calculer_masse_cuivre_kg,
    calculer_nb_sps_MT_max,
    calucler_vsp,
    nb_sps_BT,
    vsp_usine,
    bmax_calc,
    nb_sps_mt,
    nb_sps_max,
    rapport_tensions,
    rapport_transformation,
    Poids_bobinage_effectif,
    coeficient_pertes,
    coeficient_section,
    isolation_axial,
    isolation_Radiale,
    section_cond_BT,
    calcule_J_BT,
    spires_max_Bt,
    calcule_epaisseur_bt,
    calcule_epaisseur_bt_isol
)
from core.advanced_transformer_optimization import compute_mass, compute_cost, compute_losses, compute_efficiency, _objective_weighted, _temperature_constraint, optimize_transformer
from output.bom_manager import BOMManager

def calculer_tensions(user_inputs):
    """
    Utilise les fonctions du module electrical.py pour calculer
    la tension de phase primaire et secondaire en fonction des entrées utilisateur.
    """
    primary_voltage = user_inputs['primary_voltage']
    secondary_voltage = user_inputs['secondary_voltage']
    couplage_primaire = user_inputs['couplage_primaire']
    couplage_secondaire = user_inputs['couplage_secondaire']

    U1_phase = calcul_tension_1_phase(primary_voltage, couplage_primaire)
    U2_phase = calcul_tension_2_phase(secondary_voltage, couplage_secondaire)

    return U1_phase, U2_phase


def calculate_all(user_inputs):
    results = {}

    # SECTION ÉLECTRIQUE
    elec_data = calculate_electrical_params(
        power_kva=user_inputs['power_kva'],
        primary_voltage=user_inputs['primary_voltage'],
        secondary_voltage=user_inputs['secondary_voltage'],
        transformer_type=user_inputs['transformer_type'],
        couplage_primaire=user_inputs['couplage_primaire'],
        couplage_secondaire=user_inputs['couplage_secondaire']
    )
    
    results["electrical"] = elec_data
    
    # SECTION BOBINAGE (primaire et secondaire)
    V1 = user_inputs['primary_voltage']
    V2 = user_inputs['secondary_voltage']
    transformer_type = user_inputs["transformer_type"]
    S_kVA = user_inputs['power_kva']
    I1 = elec_data['I1_A']
    I2 = elec_data['I2_A']
    f = user_inputs["frequency_hz"]
    b_max = user_inputs["b_max"]  # Tesla
    Ae = 0.03  # m² (valeur fictive à remplacer par la vraie surface du noyau)
    l_moy = 0.8  # périmètre moyen d'une spire (m)
    winding_material=user_inputs['winding_material']
    cooling_bob_type=user_inputs['cooling_bob_type']
    Epaisseur =user_inputs["Epaisseur"]
    Hauteur = user_inputs["Hauteur"]
    Etage = user_inputs["Etage"]
    Nbre_cond =user_inputs["Cond"]
    sps_bt=user_inputs["Sps_bt"]
    Couche_bt=user_inputs["Couche_BT"]
    Epaisseur_Papier=user_inputs["Ep_Papier"]
    Nb_cannaux_bt =user_inputs["Nb_cannaux_bt"]
    Nombre_Papier =user_inputs["Nb_Papier"]
    isolement=Epaisseur_Papier * Nombre_Papier
    largeur_canal_BT=user_inputs["largeur_canal_BT"]
    depart=user_inputs["depart"]
    dis_circuit_bt1=user_inputs["dis_circuit_bt1"]
    nbre_cannaux_BT_isol= 1
 
    # Primaire
    N1 = compute_number_of_turns(V1, f, b_max, Ae)
    S1 = compute_conductor_section(I1)
    L1 = compute_conductor_length(N1, l_moy)
    R1 = compute_resistance(1.68e-8, L1, S1)
    Pcu1 = compute_copper_losses(I1, R1)
    mcu1 = compute_copper_mass(L1, S1)

    # Secondaire
    N2 = compute_number_of_turns(V2, f, b_max, Ae)
    S2 = compute_conductor_section(I2)
    L2 = compute_conductor_length(N2, l_moy)
    R2 = compute_resistance(1.68e-8, L2, S2)
    Pcu2 = compute_copper_losses(I2, R2)
    mcu2 = compute_copper_mass(L2, S2)
    courant_bt=calculer_courant_bt(puissance_kVA=user_inputs["power_kva"], tension_BT=V2)
    courant_ht= calculer_courant_ht(S_kVA,V1,transformer_type)
    sps_max=calculer_nb_sps_MT_max(spires_par_volt=0.8,tension_MT=V1)
    spire_bt=calculer_nbre_spires_BT(sps_max, tension_BT=V2,tension_MT=V1)
    conducteur_section=compute_conductor_section(courant_ht, J=3)
    vsp=calucler_vsp(f,b_max)
    V1 = user_inputs['primary_voltage']
    V2 = user_inputs['secondary_voltage']
    couplage_primaire = user_inputs['couplage_primaire']
    couplage_secondaire = user_inputs['couplage_secondaire']

    # 🔁 Calcul des tensions de phase
    U1_phase = calcul_tension_1_phase(V1, couplage_primaire)
    U2_phase = calcul_tension_2_phase(V2, couplage_secondaire)
    nbs_sps_bt=nb_sps_BT(U2_phase,vsp)
    sps_bt_def=41
    variation=1
    reglage=5
    vsp_sacem=vsp_usine(U2_phase,sps_bt_def=41)
    b_max_calc=bmax_calc(vsp_sacem,f)
    sps_mt_calc=nb_sps_mt(V1,vsp_sacem)
    sps_max=nb_sps_max(sps_mt_calc,reglage)
    rapport_transformations=rapport_transformation(sps_mt_calc,sps_bt_def)
    rapport_tension=rapport_tensions(V1,U2_phase)
    cef_poids= Poids_bobinage_effectif(winding_material)
    coef_perte=coeficient_pertes(winding_material)
    Coef_Section = coeficient_section(cooling_bob_type)
    isol_axial = isolation_axial(cooling_bob_type)
    isol_radial = isolation_Radiale(cooling_bob_type)
    calc_section_cond_bt = section_cond_BT (Hauteur,Epaisseur,Etage,Nbre_cond)
    J_BT = calcule_J_BT(U2_phase,calc_section_cond_bt)
    spires_maxBt =spires_max_Bt(sps_bt,Couche_bt)
    epaisseur_BT=calcule_epaisseur_bt(isol_radial,Etage,cooling_bob_type,Epaisseur,Nbre_cond,Couche_bt,largeur_canal_BT,isolement,Nb_cannaux_bt)
    epaisseur_BT_isol=calcule_epaisseur_bt_isol(isol_radial,Etage,cooling_bob_type,Epaisseur,Nbre_cond,Couche_bt,largeur_canal_BT,isolement,nbre_cannaux_BT_isol)
    epaisseur_BT_Moyene= (epaisseur_BT + epaisseur_BT_isol)/2
    eppaisseur_BTT=calculer_epaisseur_bobine_BT(Couche_bt, Epaisseur, isolement, Nb_cannaux_bt, largeur_canal_BT)
    Epaisseur_isolement=calculer_epaisseur_isolement(Nombre_Papier, Epaisseur_Papier, isolement)


    winding_data = {
    "N1_spires": round(N1),
    "N2_spires": round(N2),
    "section_1_mm2": round(S1, 2),
    "section_2_mm2": round(S2, 2),
    "longueur_fil_1_m": round(L1, 1),
    "longueur_fil_2_m": round(L2, 1),
    "resistance_1_ohm": round(R1, 4),
    "resistance_2_ohm": round(R2, 4),
    "pertes_cuivre_1_W": round(Pcu1, 2),
    "pertes_cuivre_2_W": round(Pcu2, 2),
    "masse_cuivre_1_kg": round(mcu1, 2),
    "masse_cuivre_2_kg": round(mcu2, 2),
    "masse_cuivre_totale_kg": round(mcu1 + mcu2, 2),
    "courant_bt":courant_bt,
    "courant_ht":courant_ht,
    "sps_max":sps_max,
    "spire_bt":round(spire_bt),
    "conducteur_section":conducteur_section,
    "vsp":vsp,
    "U2_phase": U2_phase,
    "U1_phase": U1_phase,
    "nbs_sps_bt" : nbs_sps_bt,
    "sps_bt_def" : sps_bt_def,
    "vsp_sacem"  : vsp_sacem,
    "b_max_calc" : b_max_calc,
    "sps_mt_calc" : sps_mt_calc,
    "variation" : variation,
    "reglage" : reglage,
    "sps_max" : sps_max,
    "rapport_transformation" : rapport_transformations,
    "rapport_tension" : rapport_tension,
    "Poids_bobinage_effectif" :cef_poids,
    "Coeficient_pertes" : coef_perte,
    "Coeficient_section" : Coef_Section,
    "Isolation_Axial"  :isol_axial,
    "Isolation_Radial" : isol_radial,
    "Section_cond_bt" : calc_section_cond_bt,
    "Calc_J_BT" : J_BT,
    "winding_material" : winding_material,
    "cooling_bob_type" : cooling_bob_type,
    "spires_max_Bt" : spires_maxBt,
    "Ep_Papier" : Epaisseur_Papier,
    "Epaisseur" :Epaisseur,
    "Hauteur" :Hauteur,
    "Cond" : Nbre_cond,
    "Etage" : Etage,
    "Couche_bt" : Couche_bt,
    "Nb_Papier" : Nombre_Papier,
    "isolement_bt" : isolement,
    "Nb_cannaux_bt" : Nb_cannaux_bt,
    "largeur_canal_BT" : largeur_canal_BT,
    "epaisseur_BT" : epaisseur_BT,
    "epaisseur_BT_isol" : epaisseur_BT_isol,
    "depart" : depart,
    "dis_circuit_bt1" : dis_circuit_bt1,
    "nbre_cannaux_BT_isol" : nbre_cannaux_BT_isol,
    "epaisseur_BT_Moyene" : epaisseur_BT_Moyene,
    "eppaisseur_BTT"  : eppaisseur_BTT,
    "Epaisseur_isolement" : Epaisseur_isolement,


}
    results["winding"] = winding_data


    # SECTION GÉOMÉTRIE
    core_type = 'EI' if user_inputs['core_material'] == 'Acier électrique' else 'Autre'
    core_geom = get_standard_core_dimensions(core_type, user_inputs['power_kva'])
    tank_geom = TankGeometry('rectangulaire', 1000, 800, 600)

    geom_data = {
        'core_weight_kg': core_geom.core_area_mm2() * 7.65e-4,
        'tank_surface_m2': tank_geom.surface_area_mm2() / 1e6,
        'tank_volume_liters': tank_geom.volume_liters()
    }
    results["geometry"] = geom_data
    

    # SECTION MÉCANIQUE
    h, w, d = 0.6, 0.8, 1.0  # En mètres
    
    tank_surface = calculate_tank_surface_m2(h, w, d)
    tank_mass = calculate_tank_mass_kg(h, w, d)
    mech_data = {
        'tank_surface_m21': tank_surface,
        'tank_surface_m2': calculate_tank_surface_m2(h, w, d),
        'tank_mass_kg': calculate_tank_mass_kg(h, w, d),
        'paint_liters': calculate_paint_required_liters(calculate_tank_surface_m2(h, w, d)),
        'accessory_mass_kg': estimate_accessory_mass_kg(tank_mass),
    }
    mech_data['total_mechanical_mass_kg'] = calculate_total_mechanical_mass_kg(
        mech_data['tank_mass_kg'], mech_data['accessory_mass_kg']
    )
    results["mechanical"] = mech_data

    # SECTION THERMIQUE
    p_cu = elec_data['losses_copper_W']
    p_fe = elec_data['losses_core_W']
    total_loss = total_losses(p_cu, p_fe)

    # Caractéristique de convection (pour convection naturelle air externe)
    char_length_m = mech_data.get('char_length_m', 1.0)
    surface_m2 = mech_data['tank_surface_m2']

    # Convection naturelle air
    temp_rise_conv = calculate_temp_rise_convection(total_loss, surface_m2, char_length_m)
    final_temp = calculate_final_temperature(ambient_temp_c=25, temp_rise_c=temp_rise_conv)

    # Vérification classe de refroidissement
    cooling_ok = cooling_class_check(temp_rise_conv, user_inputs.get('cooling_type', 'A')[0])

    # Calcul thermique ONAN (huile)
    oil_mass_kg = mech_data.get('oil_mass_kg', 280)
    oil_specific_heat = 1900  # J/kg·K
    delta_t_oil = calculate_oil_temp_rise_ONAN(
    losses_w=total_loss,
    oil_mass_kg=oil_mass_kg,
    oil_specific_heat=oil_specific_heat,
    surface_m2=surface_m2,
    ambient_temp_c=25
    )
    hotspot_temp = estimate_hotspot_temperature_ONAN(ambient_temp_c=25, delta_t_top_oil=delta_t_oil)

    # Regroupement des résultats
    thermal_data = {
    'losses_total_W': total_loss,
    'temp_rise_conv_C': round(temp_rise_conv, 2),
    'final_temp_C': round(final_temp, 2),
    'is_within_class': cooling_ok,
    'oil_temp_rise_ONAN_C': round(delta_t_oil, 2),
    'hotspot_temp_ONAN_C': round(hotspot_temp, 2),
}

    # Ajout au dictionnaire global
    results["thermal"] = thermal_data


    # SECTION OPTIMISATION
    from core.optimization import optimize_transformer_multi
    
    optimization_result = optimize_transformer_multi(
        voltage=user_inputs['primary_voltage'],
        power=user_inputs['power_kva'] * 1000,
        weights=(0.4, 0.4, 0.2)
    )
    results["optimization"] = optimization_result

    # Définitions nécessaires pour l’innovation
    voltage_V = user_inputs['primary_voltage']
    power_W = user_inputs['power_kva'] * 1000 
    # Masse de cuivre réelle
    cu_section_mm2 = optimization_result["section_cuivre_mm2"]
    cu_length_m = 200
    cu_density = 8.9
    cu_mass_kg = (cu_section_mm2 * 1e-2) * cu_length_m * cu_density / 1000
    results["copper_mass_kg"] = cu_mass_kg
    #innovation decision
    if "courant_A" in optimization_result:
     current = optimization_result["courant_A"]
    else:
     voltage_V = user_inputs['primary_voltage']
     current = power_W / (voltage_V * 1.732)  # Triphasé par défaut
       # SECTION INNOVATION

    losses_W = optimization_result["pertes_totales_W"]  # Doit exister dans l'output
    mass_fe = optimization_result.get("masse_fer_kg", 100)  # Valeur par défaut si absente
    
    section = cu_section_mm2
    volume_cu = optimization_result.get("volume_cuivre_mm3", cu_section_mm2 * cu_length_m * 1e3)
    vol_slot = optimization_result.get("volume_encoche_mm3", volume_cu * 1.2)  # Exemple

    # Appel à la fonction innovation
    innovation_result = innovation_decision_assistant(
    power_W, losses_W, cu_mass_kg, mass_fe, current, section, volume_cu, vol_slot
)

    results["innovations"] = innovation_result

    # SECTION BOM
    bom_inputs = {
        'core_weight_kg': geom_data['core_weight_kg'],
        'primary_winding_mass_kg': cu_mass_kg / 2,
        'secondary_winding_mass_kg': cu_mass_kg / 2,
        'tank_volume_liters': geom_data['tank_volume_liters'],
        'power_kva': user_inputs['power_kva']
    }

    bom_manager = BOMManager()
    bom_manager.set_material_config(user_inputs['winding_material'])
    bom_df = bom_manager.generate_bom(bom_inputs)
    results["bom"] = bom_df
    results["bom_cost"] = bom_manager.calculate_total_cost(bom_df)
    co2 = calculate_co2_footprint(
    mass_cu_kg=cu_mass_kg,
    mass_fe_kg=geom_data['core_weight_kg']
)
    results["co2"] = co2

    results["lifetime_cost_eur"] = calculate_lifetime_cost(
    initial_cost=results["bom_cost"],
    annual_losses_W=results["thermal"]["losses_total_W"]
)

    results["improved_efficiency_percent"] = improved_efficiency(
    power_W=user_inputs['power_kva'] * 1000,
    losses_total_W=results["thermal"]["losses_total_W"]
)

    results["suggested_cooling_class"] = cooling_class_suggestion(
    results["thermal"]["temp_rise_conv_C"]
)

    return results
