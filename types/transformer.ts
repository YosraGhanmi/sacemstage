export interface TransformerInputs {
  project: string
  installation: string
  client: string
  type: string
  power_kva: number
  primary_voltage: number
  secondary_voltage: number
  frequency_hz: number
  transformer_type: string
  winding_material: string
  b_max: number
}

export interface ElectricalResults {
  "Tension secondaire phase (V)": number
  "CourantPrim": number
  "CourantSec": number
  losses_copper_W: number
  losses_core_W: number
}

export interface WindingResults {
  "Nombre de spires primaire": number
  "Nombre de spires secondaire": number
  "Section conducteur primaire (mm²)": number
  "Section conducteur secondaire (mm²)": number
}

export interface ThermalResults {
  losses_total_W: number
  "echauffement1": number
  "Classe thermique": string
}

export interface MechanicalResults {
  "Poids total (kg)": number
  "Dimensions (mm)": string
}

export interface GeometryResults {
  core_weight_kg: number
}

export interface CO2Results {
  "Empreinte carbone (kg CO2)": number
  "Recyclabilité (%)": number
}

export interface InnovationResults {
  "Efficacité énergétique": string
  "Innovation score": number
}

export interface BOMItem {
  component: string
  quantity: number
  unit_cost: number
  total_cost: number
}

export interface TransformerResults {
  copper_mass_kg: number
  improved_efficiency_percent: number
  lifetime_cost_eur: number
  electrical: ElectricalResults
  winding: WindingResults
  thermal: ThermalResults
  mechanical: MechanicalResults
  geometry: GeometryResults
  co2: CO2Results
  innovations: InnovationResults
  bom: BOMItem[]
  bom_cost: number
  suggested_cooling_class: string
}

export interface OptimizationVariant {
  nom: string
  coût: number
  rendement: number
  poids: number
  pertes: number
  score: number
  details: {
    b_max: number
    copper_mass: number
    core_type: string
    cooling_class: string
  }
}

export interface OptimizationCriteria {
  cost: boolean
  efficiency: boolean
  weight: boolean
  losses: boolean
}

// Export all types as a default export as well
export type {
  TransformerInputs as Inputs,
  TransformerResults as Results,
  OptimizationVariant as Variant,
  OptimizationCriteria as Criteria,
  BOMItem as BOM,
}
