import type { TransformerInputs, TransformerResults } from "./types"

export class PDFFieldMapper {
  private readonly FIELD_MAP = {
    // Champs d'en-tête
    nom_client: "client",
    nom_projet: "reference",
    type_installation: "installation",
    Date: "Date",
    reference: "reference",
    revision: "revision",
    // Caractéristiques électriques - FIXED: Added proper mapping for primary/secondary voltages
    puissance_kva: "kVA",
    frequence_hz: "frequence",
    tension_primaire: "U1n",
    tension_secondaire: "U20",
    elevation_temperature_max: "echauffement2",
    
    //couplage_primaire: "Couplage",

    // Paramètres techniques
    materiau_noyau: "ClU",
    densite_courant: "Densite",
    b_max: "Induction",
    type_tole: "ToleMagnetique",
    materiau_enroulement: "NatureBob",

    // Pertes et performances
    pertes_fer: "PerteVide",
    courant_vide: "I0Vide",
    pertes_cuivre: "Pcc",
    tension_court_circuit: "Ucc",
    pertes_totales: "PertesTot",
    Echauffement: "echauffement1",

    tensionLignePrim: "tensionLignePrim",
    tensionLigneSec: "tensionLigneSec",
    tensionPhasePrim: "tensionPhasePrim",
    tensionPhaseSec: "tensionPhaseSec",
    CourantLignePrim: "CourantLignePrim",
    CourantLigneSec: "CourantLigneSec",
    CourantPhasePrim: "CourantPhasePrim",
    CourantPhaseSec: "CourantPhaseSec",
    ClasseTensionPrim: "ClasseTensionPrim",
    ClasseTensionSec: "ClasseTensionSec",
    ClasseTensionlast: "classeTensionlast",

    // Calculs de bobinage
    largeurA: "largeurA",
    largeurB: "largeurB",
    largeurC: "largeurC",
    largeurD: "largeurD",
    largeurE: "largeurE",
    largeurF: "largeurF",
    largeurG: "largeurG",
    largeurH: "largeurH",
    largeurI: "largeurI",
    largeurJ: "largeurJ",
    largeurK: "largeurK",

    gradinA: "gradinA",
    gradinB: "gradinB",
    gradinC: "gradinC",
    gradinD: "gradinD",
    gradinE: "gradinE",
    gradinF: "gradinF",
    gradinG: "gradinG",
    gradinH: "gradinH",
    gradinI: "gradinI",
    gradinJ: "gradinJ",
    gradinK: "gradinK",

    // Géométrie du noyau
    ColonnesSnette: "ColonnesSnette",
    ColonnesBT: "ColonnesBT",
    ColonnesMasse: "ColonnesMasse",
    "4emeColonneSnette": "4emeColonneSnette",
    "4emeColonneMasse": "4emeColonneMasse",
    CulasseSnette: "CulasseSnette",
    CulasseBT: "CulasseBT",
    CulasseMasse: "CulasseMasse",
    EPCM: "EPCM",
    MasseCulplusCol: "MasseCulplusCol",
    MasseTotale: "MasseTotale",

    // Paramètres de bobinage
    BobSectionduConducteurprim1: "BobSectionduConducteurprim1",
    BobSectionduConducteurSec: "BobSectionduConducteurSec",
    DensiteCourantPrim: "DensiteCourantPrim",
    DensiteCourantSec: "DensiteCourantSec",
    nbCoucherPrim: "nbCoucherPrim",
    nbCoucherSec: "nbCoucherSec",
    SpiresCouchePrim: "SpiresCouchePrim",
    SpiresCoucheSec: "SpiresCoucheSec",

    // Paramètres de court-circuit
    PCC75: "PCC75",
    addi: "addi",
    Ucca: "Ucca",
    Uccr: "Uccr",
    Ucc75: "Ucc75",
    UccCorrigee: "UccCorrigee",
    ResistanceBT75: "ResistanceBT75",
    ResistanceMT75: "ResistanceMT75",

    "spiresVsp": "spiresVsp",
    N1: "SpiresN1",
    N2: "SpiresN2",
  }

  mapperVersChampsPDF(entrees: TransformerInputs, resultats: TransformerResults): Record<string, any> {
    const donneesPDF: Record<string, any> = {}

    donneesPDF["type"] = this.composerChampInstallation(entrees)
    donneesPDF["Couplage"] = this.composercouplage(entrees)
    donneesPDF["ToleMagn"] = this.composerToleMagn(entrees)
    // Mapper les valeurs d'entrée
    Object.entries(entrees).forEach(([cle, valeur]) => {
      const champPDF = this.FIELD_MAP[cle as keyof typeof this.FIELD_MAP]
      if (champPDF) {
        donneesPDF[champPDF] = this.formaterValeur(valeur)
      }
    })

    // Mapper les résultats calculés
    this.mapperResultatsCalcules(resultats, donneesPDF)

    // Ajouter la date actuelle
    donneesPDF["Date"] = new Date().toLocaleDateString("fr-FR")

    return donneesPDF
  }
  composerToleMagn(entrees: TransformerInputs): string {
    const{type_tole,
    }= entrees
    return `${type_tole}`
  }
  composercouplage(entrees: TransformerInputs): string {
    const {
      couplage_primaire,
      couplage_secondaire,
      indice_horaire
    } = entrees

    return `${couplage_primaire}${couplage_secondaire}${indice_horaire}`
  }

  private composerChampInstallation(entrees: TransformerInputs): string {
    const {
      puissance_kva,
      type_transformateur,
      configuration,
      type_circuit_magnetique,
    } = entrees

    return `Transformateur ${configuration || "Triphasé"} ${puissance_kva} kVA à ${type_circuit_magnetique || "3 colonnes"} ${type_transformateur || "Hermétique"}`
  }

  private mapperResultatsCalcules(resultats: TransformerResults, donneesPDF: Record<string, any>) {
    // Mapper les résultats électriques
    Object.entries(resultats.electrique).forEach(([cle, valeur]) => {
      const champPDF = this.FIELD_MAP[cle as keyof typeof this.FIELD_MAP]
      if (champPDF) {
        donneesPDF[champPDF] = this.formaterValeur(valeur)
      } else {
        // Direct mapping for fields that match exactly
        donneesPDF[cle] = this.formaterValeur(valeur)
      }
    })

    // Mapper les résultats de bobinage
    Object.entries(resultats.bobinage).forEach(([cle, valeur]) => {
      const champPDF = this.FIELD_MAP[cle as keyof typeof this.FIELD_MAP]
      if (champPDF) {
        donneesPDF[champPDF] = this.formaterValeur(valeur)
      } else {
        donneesPDF[cle] = this.formaterValeur(valeur)
      }
    })

    // Mapper les résultats de géométrie
    Object.entries(resultats.geometrie).forEach(([cle, valeur]) => {
      const champPDF = this.FIELD_MAP[cle as keyof typeof this.FIELD_MAP]
      if (champPDF) {
        donneesPDF[champPDF] = this.formaterValeur(valeur)
      } else {
        donneesPDF[cle] = this.formaterValeur(valeur)
      }
    })

    // Mapper les résultats thermiques
    Object.entries(resultats.thermique).forEach(([cle, valeur]) => {
      const champPDF = this.FIELD_MAP[cle as keyof typeof this.FIELD_MAP]
      if (champPDF) {
        donneesPDF[champPDF] = this.formaterValeur(valeur)
      } else {
        donneesPDF[cle] = this.formaterValeur(valeur)
      }
    })
  }

  private formaterValeur(valeur: any): string {
    if (typeof valeur === "number") {
      return Number.isInteger(valeur) ? valeur.toString() : valeur.toFixed(2)
    }
    return String(valeur)
  }

  // Générer un rapport de mappage des champs pour le débogage
  genererRapportMappageChamps(entrees: TransformerInputs, resultats: TransformerResults): string {
    const donneesPDF = this.mapperVersChampsPDF(entrees, resultats)

    let rapport = "=== RAPPORT DE MAPPAGE DES CHAMPS PDF ===\n\n"

    Object.entries(donneesPDF).forEach(([champPDF, valeur]) => {
      rapport += `Champ PDF: "${champPDF}" = "${valeur}"\n`
    })

    rapport += "\n=== CHAMPS D'ENTRÉE NON MAPPÉS ===\n"
    Object.keys(entrees).forEach((cle) => {
      if (!this.FIELD_MAP[cle as keyof typeof this.FIELD_MAP]) {
        rapport += `Champ d'entrée "${cle}" n'a pas de mappage PDF\n`
      }
    })

    return rapport
  }
}