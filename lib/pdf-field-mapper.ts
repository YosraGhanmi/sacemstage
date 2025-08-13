import type { TransformerInputs, TransformerResults } from "./types"

export class PDFFieldMapper {
  // Complete field mapping between your UI and PDF form
  private readonly FIELD_MAP = {
    // Header fields
    client_name: "client",
    project_name: "reference",
    transformer_type: "type",
    installation_type: "installation",
    Date: "Date",
    reference: "reference",
    revision: "revision",

    // Electrical characteristics
    power_kva: "kVA",
    frequency_hz: "frequence",
    primary_voltage: "U1n(V)",
    secondary_voltage: "U20 (V)",
    max_temperature_rise: "Variation",
    primary_coupling: "Couplage",

    // Technical parameters
    core_material: "ClU(KV)",
    current_density: "Densite",
    b_max: "Induction",
    sheet_type: "ToleMagnetique",
    winding_material: "NatureBob",
    cooling_type: "DureeCC",

    // Losses and performance
    core_losses: "PerteVide",
    no_load_current: "I0Vide",
    copper_losses: "Pcc",
    short_circuit_voltage: "Ucc",
    total_losses: "PertesTot",
    temperature_rise: "echauffement",

    // Calculated electrical values
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
    ClasseTensionlast: "ClasseTensionlast",

    // Winding calculations
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

    // Core geometry
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

    // Winding parameters
    BobSectionduConducteurprim1: "BobSectionduConducteurprim1",
    BobSectionduConducteurSec: "BobSectionduConducteurSec",
    DensiteCourantPrim: "DensiteCourantPrim",
    DensiteCourantSec: "DensiteCourantSec",
    nbCoucherPrim: "nbCoucherPrim",
    nbCoucherSec: "nbCoucherSec",
    SpiresCouchePrim: "SpiresCouchePrim",
    SpiresCoucheSec: "SpiresCoucheSec",

    // Short circuit parameters
    PCC75: "PCC75",
    addi: "addi",
    Ucca: "Ucca",
    Uccr: "Uccr",
    Ucc75: "Ucc75",
    UccCorrigee: "UccCorrigee",
    ResistanceBT75: "ResistanceBT75",
    ResistanceMT75: "ResistanceMT75",
  }

  mapToPDFFields(inputs: TransformerInputs, results: TransformerResults): Record<string, any> {
    const pdfData: Record<string, any> = {}

    // Map input values
    Object.entries(inputs).forEach(([key, value]) => {
      const pdfField = this.FIELD_MAP[key as keyof typeof this.FIELD_MAP]
      if (pdfField) {
        pdfData[pdfField] = this.formatValue(value)
      }
    })

    // Map calculated results
    this.mapCalculatedResults(results, pdfData)

    // Add current date
    pdfData["Date"] = new Date().toLocaleDateString("fr-FR")

    return pdfData
  }

  private mapCalculatedResults(results: TransformerResults, pdfData: Record<string, any>) {
    // Map electrical results
    Object.entries(results.electrical).forEach(([key, value]) => {
      const pdfField = this.FIELD_MAP[key as keyof typeof this.FIELD_MAP]
      if (pdfField) {
        pdfData[pdfField] = this.formatValue(value)
      }
    })

    // Map winding results
    Object.entries(results.winding).forEach(([key, value]) => {
      const pdfField = this.FIELD_MAP[key as keyof typeof this.FIELD_MAP]
      if (pdfField) {
        pdfData[pdfField] = this.formatValue(value)
      }
    })

    // Map geometry results
    Object.entries(results.geometry).forEach(([key, value]) => {
      const pdfField = this.FIELD_MAP[key as keyof typeof this.FIELD_MAP]
      if (pdfField) {
        pdfData[pdfField] = this.formatValue(value)
      }
    })

    // Map thermal results
    Object.entries(results.thermal).forEach(([key, value]) => {
      const pdfField = this.FIELD_MAP[key as keyof typeof this.FIELD_MAP]
      if (pdfField) {
        pdfData[pdfField] = this.formatValue(value)
      }
    })
  }

  private formatValue(value: any): string {
    if (typeof value === "number") {
      return Number.isInteger(value) ? value.toString() : value.toFixed(2)
    }
    return String(value)
  }

  // Generate field mapping for debugging
  generateFieldMappingReport(inputs: TransformerInputs, results: TransformerResults): string {
    const pdfData = this.mapToPDFFields(inputs, results)

    let report = "=== PDF FIELD MAPPING REPORT ===\n\n"

    Object.entries(pdfData).forEach(([pdfField, value]) => {
      report += `PDF Field: "${pdfField}" = "${value}"\n`
    })

    report += "\n=== UNMAPPED INPUT FIELDS ===\n"
    Object.keys(inputs).forEach((key) => {
      if (!this.FIELD_MAP[key as keyof typeof this.FIELD_MAP]) {
        report += `Input field "${key}" has no PDF mapping\n`
      }
    })

    return report
  }
}
