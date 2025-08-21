import type { TransformerInputs, TransformerResults } from "./types"

export class TransformerCalculator {
  private entrees: TransformerInputs

  constructor(entrees: TransformerInputs) {
    this.entrees = entrees
  }

  // Constants (from XLSM data & transformer engineering refs)
  private readonly RESISTIVITY_CU = 1.724e-8 // Ω·m at 20°C
  private readonly RESISTIVITY_AL = 2.82e-8 // Ω·m at 20°C
  private readonly TEMP_COEFF_RESISTIVITY = 0.00393
  private readonly DENSITY_CU = 8900 // kg/m³
  private readonly DENSITY_AL = 2700 // kg/m³
  private readonly STACKING_FACTOR = 0.9

  private readonly CORE_LOSS_TABLE: Record<string, number> = {
    // W/kg at Bmax=1.5T from XLSM
    "0.27mm": 0.85,
    "0.30mm": 0.95,
    "0.35mm": 1.1,
    HiB: 0.75,
  }

  calculerTout(): TransformerResults {
    const electrique = this.calculerElectrique()
    const bobinage = this.calculerBobinage()
    const thermique = this.calculerThermique()
    const mecanique = this.calculerMecanique()
    const geometrie = this.calculerGeometrie()

    return {
      masse_cuivre_kg: this.calculerPoidsCuivre(),
      rendement_ameliore_pourcent: this.calculerRendement(),
      cout_vie_eur: this.calculerCoutVie(),
      electrique,
      bobinage,
      thermique,
      mecanique,
      geometrie,
      co2: this.calculerImpactCO2(),
      innovations: this.calculerInnovations(),
      nomenclature: this.calculerNomenclature(),
      cout_nomenclature: this.calculerCoutNomenclature(),
      classe_refroidissement_suggeree: this.suggererClasseRefroidissement(),
    }
  }

  private calculerElectrique() {
    const { puissance_kva, tension_primaire, tension_secondaire, frequence_hz } = this.entrees

    const courantPrim = this.calculerCourantLignePrimaire()
    const courantSec = this.calculerCourantLigneSecondaire()

    const tensionPhasePrim = this.calculerTensionPhasePrimaire()
    const tensionPhaseSec = this.calculerTensionPhaseSecondaire()

    const pertesCuivre = this.calculerPertesCuivre()
    const pertesFer = this.calculerPertesFer()

    return {
      tensionLignePrim: tension_primaire,
      tensionLigneSec: tension_secondaire,
      tensionPhasePrim,
      tensionPhaseSec,
      CourantLignePrim: courantPrim,
      CourantLigneSec: courantSec,
      CourantPhasePrim: courantPrim,
      CourantPhaseSec: courantSec,
      ClasseTensionPrim: this.calculerClasseTensionPrimaire(),
      ClasseTensionSec: this.calculerClasseTensionSecondaire(),
      classeTensionlast: this.obtenirClasseTension(Math.max(tension_primaire, tension_secondaire)),
      pertes_cuivre_W: pertesCuivre,
      pertes_fer_W: pertesFer,
    }
  }

  private calculerBobinage() {
    const { tension_primaire, tension_secondaire, frequence_hz, b_max, puissance_kva, materiau_enroulement } =
      this.entrees

    const voltsParSpire = this.calculerVoltsParSpire()

    const rapportSpires = tension_primaire / tension_secondaire
    const nombreSpiresPrim = this.calculerNombreSpiresPrimaire()
    const nombreSpiresSec = this.calculerNombreSpiresSecondaire()

    const sectionConducteurPrim = this.calculerSectionConducteurPrimaire()
    const sectionConducteurSec = this.calculerSectionConducteurSecondaire()

    return {
      "Nombre de spires primaire": nombreSpiresPrim,
      "Nombre de spires secondaire": nombreSpiresSec,
      "Section conducteur primaire (mm²)": sectionConducteurPrim,
      "Section conducteur secondaire (mm²)": sectionConducteurSec,
      "spiresVsp": voltsParSpire,
      N1: nombreSpiresPrim,
      N2: nombreSpiresSec,
      BobSectionduConducteurprim1: sectionConducteurPrim,
      BobSectionduConducteurSec: sectionConducteurSec,
      DensiteCourantPrim: this.calculerDensiteCourantPrimaire(),
      DensiteCourantSec: this.calculerDensiteCourantSecondaire(),
    }
  }

  private calculerThermique() {
    const pertesTotales = this.calculerPertesTotales()
    const temperatureMax = this.calculerTemperatureMax()

    return {
      pertes_totales_W: pertesTotales,
      "Température max (°C)": Math.round(temperatureMax),
      "Classe thermique": this.obtenirClasseThermique(temperatureMax),
      Echauffement: this.calculerEchauffement(),
    }
  }

  private calculerMecanique() {
    const poidsTotalKg = this.calculerPoidsTotalKg()
    const dimensions = this.calculerDimensions(this.entrees.puissance_kva)

    return {
      "Poids total (kg)": Math.round(poidsTotalKg),
      "Dimensions (mm)": dimensions,
      MasseTotale: Math.round(poidsTotalKg),
    }
  }

  private calculerGeometrie() {
    const { puissance_kva, b_max, type_tole } = this.entrees

    const poidsFer = this.calculerPoidsFer()
    const surfaceNoyau = puissance_kva * 15

    return {
      poids_fer_kg: Math.round(poidsFer * 10) / 10,
      ColonnesSnette: surfaceNoyau,
      ColonnesBT: b_max,
      ColonnesMasse: poidsFer * 0.6,
      "4emeColonneSnette": surfaceNoyau * 0.8,
      "4emeColonneMasse": poidsFer * 0.2,
      CulasseSnette: surfaceNoyau * 1.2,
      CulasseBT: b_max * 0.9,
      CulasseMasse: poidsFer * 0.4,
      EPCM: 0.35,
      MasseCulplusCol: poidsFer,
      MasseTotale: poidsFer,
    }
  }

  private calculerImpactCO2() {
    const { puissance_kva } = this.entrees
    const empreinte = puissance_kva * 1.25
    return {
      "Empreinte carbone (kg CO2)": Math.round(empreinte * 10) / 10,
      "Recyclabilité (%)": 85,
    }
  }

  private calculerInnovations() {
    const rendement = this.calculerRendement()
    return {
      "Efficacité énergétique": rendement > 97 ? "Classe A+" : rendement > 95 ? "Classe A" : "Classe B",
      "Score innovation": Math.round((rendement - 90) * 10) / 10,
    }
  }

  private calculerNomenclature() {
    const { puissance_kva, materiau_enroulement } = this.entrees
    const prixCuivre = materiau_enroulement === "cuivre" ? 8.5 : 6.2
    return [
      {
        composant: "Noyau magnétique",
        quantite: 1,
        cout_unitaire: puissance_kva * 4.5,
        cout_total: puissance_kva * 4.5,
      },
      {
        composant: `${materiau_enroulement} primaire`,
        quantite: Math.round(puissance_kva * 0.25),
        cout_unitaire: prixCuivre,
        cout_total: Math.round(puissance_kva * 0.25 * prixCuivre * 100) / 100,
      },
      {
        composant: `${materiau_enroulement} secondaire`,
        quantite: Math.round(puissance_kva * 0.2),
        cout_unitaire: prixCuivre,
        cout_total: Math.round(puissance_kva * 0.2 * prixCuivre * 100) / 100,
      },
      {
        composant: "Isolation",
        quantite: 1,
        cout_unitaire: puissance_kva * 0.85,
        cout_total: puissance_kva * 0.85,
      },
    ]
  }

  private calculerCoutNomenclature(): number {
    return this.calculerNomenclature().reduce((somme, item) => somme + item.cout_total, 0)
  }

  private calculerCoutVie(): number {
    const { puissance_kva } = this.entrees
    const coutInitial = this.calculerCoutNomenclature()
    const coutFonctionnement = puissance_kva * 15 * 20
    return Math.round(coutInitial + coutFonctionnement)
  }

  private suggererClasseRefroidissement(): string {
    const { puissance_kva, type_refroidissement } = this.entrees
    if (type_refroidissement) return type_refroidissement
    if (puissance_kva <= 100) return "AN"
    if (puissance_kva <= 500) return "ONAN"
    if (puissance_kva <= 1000) return "ONAN+"
    return "ONAF"
  }

  private calculerChampInstallation(): string {
    const {
      puissance_kva,
      type_transformateur,
      configuration,
      type_circuit_magnetique,
    } = this.entrees

    return `Transformateur ${configuration || "Triphasé"} ${puissance_kva} kVA à ${type_circuit_magnetique || "3 colonnes"} ${type_transformateur || "Hermétique"}`
  }

  // Fonctions de calcul modulaires pour chaque champ de sortie

  calculerTensionLignePrimaire(): number {
    return this.entrees.tension_primaire
  }

  calculerTensionLigneSecondaire(): number {
    return this.entrees.tension_secondaire
  }

  calculerTensionPhasePrimaire(): number {
    return this.entrees.tension_primaire / Math.sqrt(3)
  }

  calculerTensionPhaseSecondaire(): number {
    return this.entrees.tension_secondaire / Math.sqrt(3)
  }

  calculerCourantLignePrimaire(): number {
    return (this.entrees.puissance_kva * 1000) / (this.entrees.tension_primaire * Math.sqrt(3))
  }

  calculerCourantLigneSecondaire(): number {
    return (this.entrees.puissance_kva * 1000) / (this.entrees.tension_secondaire * Math.sqrt(3))
  }

  calculerCourantPhasePrimaire(): number {
    return this.calculerCourantLignePrimaire()
  }

  calculerCourantPhaseSecondaire(): number {
    return this.calculerCourantLigneSecondaire()
  }

  calculerClasseTensionPrimaire(): string {
    return this.obtenirClasseTension(this.entrees.tension_primaire)
  }

  calculerClasseTensionSecondaire(): string {
    return this.obtenirClasseTension(this.entrees.tension_secondaire)
  }

  calculerNombreSpiresPrimaire(): number {
    const voltsParSpire = this.calculerVoltsParSpire()
    return Math.round(this.entrees.tension_primaire / voltsParSpire)
  }

  calculerNombreSpiresSecondaire(): number {
    const rapportSpires = this.entrees.tension_primaire / this.entrees.tension_secondaire
    return Math.round(this.calculerNombreSpiresPrimaire() / rapportSpires)
  }

  calculerVoltsParSpire(): number {
    const { tension_primaire, frequence_hz, b_max } = this.entrees
    return tension_primaire / (4.44 * frequence_hz * b_max * 1e-4 * Math.sqrt(3))
  }

  calculerSectionConducteurPrimaire(): number {
    return this.calculerSectionConducteur(
      this.entrees.puissance_kva,
      this.entrees.tension_primaire,
      this.entrees.materiau_enroulement,
    )
  }

  calculerSectionConducteurSecondaire(): number {
    return this.calculerSectionConducteur(
      this.entrees.puissance_kva,
      this.entrees.tension_secondaire,
      this.entrees.materiau_enroulement,
    )
  }

  calculerDensiteCourantPrimaire(): number {
    const courant = this.calculerCourantLignePrimaire()
    const section = this.calculerSectionConducteurPrimaire()
    return courant / section
  }

  calculerDensiteCourantSecondaire(): number {
    const courant = this.calculerCourantLigneSecondaire()
    const section = this.calculerSectionConducteurSecondaire()
    return courant / section
  }

  calculerPertesCuivre(): number {
    const courantPrim = this.calculerCourantLignePrimaire()
    const courantSec = this.calculerCourantLigneSecondaire()
    return Math.pow(courantPrim, 2) * 0.5 + Math.pow(courantSec, 2) * 0.3
  }

  calculerPertesFer(): number {
    return this.entrees.puissance_kva * 0.8
  }

  calculerPertesTotales(): number {
    return this.calculerPertesCuivre() + this.calculerPertesFer()
  }

  calculerTemperatureMax(): number {
    const pertesTotales = this.calculerPertesTotales()
    return 75 + (pertesTotales / this.entrees.puissance_kva) * 0.05
  }

  calculerEchauffement(): number {
    return Math.round(this.calculerTemperatureMax() - 40)
  }

  calculerPoidsTotalKg(): number {
    return this.entrees.puissance_kva * 1.8 + 50
  }

  calculerPoidsCuivre(): number {
    return Math.round(this.entrees.puissance_kva * 0.45 * 10) / 10
  }

  calculerPoidsFer(): number {
    return this.entrees.puissance_kva * 0.95
  }

  calculerRendement(): number {
    const pertes = this.entrees.puissance_kva * 12
    const rendement = (1 - pertes / (this.entrees.puissance_kva * 1000)) * 100
    return Math.round(rendement * 100) / 100
  }

  // Fonctions utilitaires
  private obtenirClasseTension(tension: number): string {
    if (tension <= 1000) return "BT"
    if (tension <= 35000) return "MT"
    return "HT"
  }

  private obtenirClasseThermique(temp: number): string {
    if (temp <= 105) return "A"
    if (temp <= 120) return "E"
    if (temp <= 130) return "B"
    if (temp <= 155) return "F"
    return "H"
  }

  private calculerSectionConducteur(puissance: number, tension: number, materiau: string): number {
    const courant = (puissance * 1000) / (tension * Math.sqrt(3))
    const densite = materiau === "cuivre" ? 3.5 : 2.5
    return Math.round((courant / densite) * 100) / 100
  }

  private calculerDimensions(puissance: number): string {
    const longueur = Math.round(300 + puissance * 0.8)
    const largeur = Math.round(250 + puissance * 0.6)
    const hauteur = Math.round(400 + puissance * 0.5)
    return `${longueur}x${largeur}x${hauteur}`
  }
}
