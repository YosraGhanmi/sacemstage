export interface TransformerInputs {
  // Informations générales
  client_name: string
  project_name: string
  transformer_type: string // hermetique/respirant/H59/H61
  installation_type: string // exterieur/poteau/interieur
  
  // Bobinage
  bob_type: string // Bande/Meplat
  epaisseur: number
  hauteur: number
  cond: string
  etage: number
  couche_bt: number
  sps_bt: number
  ep_papier: number
  nb_papier: number
  isolement_bt: number
  nb_cannaux_bt: number
  largeur_canal_bt: number
  depart: string // 100/90/70/50
  dis_circuit_bt1: number
  
  // Spécifications électriques
  power_kva: number
  primary_voltage: number
  secondary_voltage: number
  frequency_hz: number
  b_max: number
  
  // Enroulements & circuit
  configuration: string // Triphasé/Monophasé
  winding_material: string // cuivre/aluminium
  primary_coupling: string // D/YN/Y/ZN/Z
  secondary_coupling: string // YN/D/Y/ZN
  
  // Noyau magnétique
  core_material: string // Acier electrique/Acier HiB
  sheet_type: string // M110-23/M120-27/etc
  magnetic_circuit_type: string // 3Colonnes/4Colonnes
  
  // Refroidissement & température
  cooling_type: string // ONAN/ONAF/ONAN+/AN
  max_temperature_rise: number
}

export interface ElectricalResults {
  "Tension secondaire phase (V)": number
  "Courant primaire (A)": number
  "Courant secondaire (A)": number
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
  "Température max (°C)": number
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
