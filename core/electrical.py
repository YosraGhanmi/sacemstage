import math


def calcul_tension_1_phase(tension_ligne, couplage_primaire):
    if couplage_primaire in ["D", "Δ"]:
        return tension_ligne
    elif couplage_primaire in ["Y", "YN"]:
        return tension_ligne / math.sqrt(3)
    elif couplage_primaire in ["Z", "ZN"]:
        return tension_ligne * 2 / 3
    else:
        raise ValueError(f"Couplage inconnu : {couplage_primaire}")

def calcul_tension_2_phase(tension_ligne, couplage_secondaire):
    if couplage_secondaire in ["D", "Δ"]:
        return tension_ligne
    elif couplage_secondaire in ["Y", "YN"]:
        return tension_ligne / math.sqrt(3)
    elif couplage_secondaire in ["Z", "ZN"]:
        return tension_ligne * 2 / 3
    else:
        raise ValueError(f"Couplage inconnu : {couplage_secondaire}")

def calcul_classe_KV(V1):
    if V1 > 24000:
        return 36
    elif V1 > 17500:
        return 24
    elif V1 > 12000:
        return 17.5
    elif V1 > 7600:
        return 12
    elif V1 > 3600:
        return 7.2
    elif V1 > 1100:
        return 3.6
    else:
        return 1.1

def get_classe_tension_secondaire(V2):
    if V2 in [400, 230]:
        return "400/230 V - standard européen"
    elif V2 == 690:
        return "690 V - usage industriel"
    elif V2 == 500:
        return "500 V - industriel spécifique"
    elif V2 == 480:
        return "480 V - norme US"
    elif V2 == 415 or V2 == 240:
        return "415/240 V - Afrique, Asie"
    elif V2 == 380 or V2 == 220:
        return "380/220 V - ancien standard"
    elif V2 == 208 or V2 == 120:
        return "208/120 V - US"
    elif V2 in [110, 115]:
        return "BT contrôle"
    elif V2 in [48, 24, 12]:
        return "Très basse tension"
    else:
        return "Tension non standard"
def tenue_f_ind(V1):
    if V1 <= 1.100:
        return 3
    elif V1 <= 3.600:
        return 10
    elif V1 <= 7.200:
        return 20
    elif V1 <= 12000:
        return 28
    elif V1 <= 17.500:
        return 38
    elif V1 <= 24000:
        return 50
    elif V1 <= 36000:
        return 70
    else:
        return None  
def tenue_choc_foudre_CEI2(V1):
    """
    Retourne la tenue au choc foudre (BIL, en kV crête) selon la norme CEI 60076-3 (CEI 2),
    à partir de la tension assignée V1_kv (en kilovolts).
    """
    if V1 <= 1.100:
        return 20
    elif V1 <= 3.600:
        return 40
    elif V1 <= 7.200:
        return 60
    elif V1 <= 12000:
        return 75
    elif V1 <= 17.500:
        return 95
    elif V1 <= 24000:
        return 125
    elif V1 <= 36000:
        return 170
    elif V1 <= 52000:
        return 250
    elif V1 <= 72.500:
        return 325
    elif V1 <= 123000:
        return 550
    elif V1 <= 145000:
        return 650
    elif V1 <= 170000:
        return 750
    elif V1 <= 245000:
        return 1050
    elif V1 <= 300000:
        return 1175
    elif V1 <= 362000:
        return 1425
    else:
        return None 

def tenue_choc_foudre_CEI1(V1):
    """
    Retourne la tenue au choc (kV crête) selon la tension assignée V1.
    """
    if V1 <= 1.100:
        return 20
    elif V1 <= 3.600:
        return 40
    elif V1 <= 7.200:
        return 60
    elif V1 <= 12000:
        return 75
    elif V1 <= 24000:
        return 95
    elif V1 <= 36000:
        return 145
    else:
        return None      

def calculate_electrical_params(power_kva, primary_voltage, secondary_voltage, transformer_type, couplage_primaire, couplage_secondaire):
    S_va = power_kva *1000
    V1 = primary_voltage
    V2 = secondary_voltage
    # Calcul Classe KV
    classe=calcul_classe_KV(V1)
    # Calcul Classe V2
    classe_V2=get_classe_tension_secondaire(V2)
    # Calcul fréquence industrielle
    tenue_ind=tenue_f_ind(V1)
    # Calcul des tensions de phase
    U1_phase = calcul_tension_1_phase(V1, couplage_primaire)
    U2_phase = calcul_tension_2_phase(V2, couplage_secondaire) 
    # Calcul des I Ligne
    I_Ligne_1=S_va/(U1_phase*math.sqrt(3))
    # Calcul des I Ligne2
    I_Ligne_2=S_va / (V2*math.sqrt(3))
    I_phase_2=I_Ligne_2
    # Calcul des I Phase
    # Calcul Tenue au choc
    tenue_choc_2=tenue_choc_foudre_CEI2(V1)
    tenue_choc_1=tenue_choc_foudre_CEI1(V1)
        # Calcul du courant de phase
    if couplage_primaire == "D":
        I_phase = I_Ligne_1 / math.sqrt(3)
    else:
        I_phase = I_Ligne_1
    # Courants
    I1 = S_va / V1
    I2 = S_va / V2

    # Estimations simples des pertes (à améliorer plus tard)
    losses_copper_W = 0.01 * S_va  # 1% de pertes cuivre
    losses_core_W = 0.004 * S_va   # 0.4% de pertes fer

    # Résistances
    R1 = 0.2
    R2 = 0.005

    # Pertes cuivre
    pertes_cuivre = round(3 * (R1 * I1**2 + R2 * I2**2), 2)
    #calcule Diametre 
    d_th = ((power_kva / 1000) ** 0.2316) * 220
    # Pertes fer
    pertes_fer = {
        "Distribution": 800,
        "Puissance": 2500,
        "Sec": 1000
    }.get(transformer_type, 1000)

    # Ucc
    ucc_percent = {
        "Distribution": 6,
        "Puissance": 10,
        "Sec": 4
    }.get(transformer_type, 6)

    # Impédance équivalente
    Z_eq = round((ucc_percent / 100) * (V1**2) / S_va, 2)

    # Chute de tension
    chute_tension = round((Z_eq * I1) / V1 * 100, 2)

    # Courant de court-circuit
    Icc = round(I1 / (ucc_percent / 100), 2)

    # Section câble recommandée
    k = 1.5
    section_cable = round(I1 / k, 2)

    # Rendement
    rendement = round((S_va - pertes_cuivre - pertes_fer) / S_va * 100, 2)

    # 🧩 Classification par niveau de puissance
    if power_kva < 1000:
        classe_puissance = "BT (basse tension)"
    elif power_kva <= 10000:
        classe_puissance = "HTA (haute tension A)"
    else:
        classe_puissance = "HTB (haute tension B)"

    # 🧩 Classification par tension primaire
    if primary_voltage < 1:
        classe_tension = "BT"
    elif primary_voltage <= 36:
        classe_tension = "HTA"
    else:
        classe_tension = "HTB"

    # Résultats complets
    return {
        "d_th" : d_th,
        "classe_v2":classe_V2,
        "classe":classe,
        "tenue à la fréquence industrielle":tenue_ind,
        "Type de transformateur": transformer_type,
        "Classe de puissance": classe_puissance,
        "Classe de tension": classe_tension,
        "tenue_choc_CEI2":tenue_choc_2,
        "tenue_choc_CEI1":tenue_choc_1,
        "Puissance (kVA)": power_kva,
        "Tension primaire (V)": V1,
        "Tension secondaire (V)": V2,
        "I_ligne_1": I_Ligne_1,
        "I_Phase_1":I_phase,
        "Tension primaire phase (V)": U1_phase,
        "Tension secondaire phase (V)": U2_phase,
        "I_ligne_2":I_Ligne_2,
        "I_Phase_2":I_phase_2,
        "I1_A": round(I1, 2),
        "I2_A": round(I2, 2),
        "Pertes cuivre (W)": pertes_cuivre,
        "Pertes fer (W)": pertes_fer,
        "Tension de court-circuit (%)": ucc_percent,
        "Impédance équivalente (Ohm)": Z_eq,
        "Chute de tension (%)": chute_tension,
        "Courant de court-circuit (A)": Icc,
        "Section de câble recommandée (mm²)": section_cable,
        "Rendement (%)": rendement,
        "losses_copper_W": round(losses_copper_W, 2),
        "losses_core_W": round(losses_core_W, 2),
        "U2_phase":U2_phase
    }
# core/electrical.py
