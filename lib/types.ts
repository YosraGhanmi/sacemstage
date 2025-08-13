export interface TransformerInputs {
  // General information
  client_name: string
  project_name: string
  transformer_type: string
  installation_type: string

  // Winding parameters
  bob_type: string
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
  depart: string
  dis_circuit_bt1: number

  // Electrical specifications
  power_kva: number
  primary_voltage: number
  secondary_voltage: number
  frequency_hz: number
  b_max: number

  // Winding & circuit
  configuration: string
  winding_material: string
  primary_coupling: string
  secondary_coupling: string

  // Core & cooling
  core_material: string
  sheet_type: string
  magnetic_circuit_type: string
  cooling_type: string
  max_temperature_rise: number
}

export interface TransformerResults {
  copper_mass_kg: number
  improved_efficiency_percent: number
  lifetime_cost_eur: number
  electrical: {
    [key: string]: number | string
  }
  winding: {
    [key: string]: number | string
  }
  thermal: {
    [key: string]: number | string
  }
  mechanical: {
    [key: string]: number | string
  }
  geometry: {
    [key: string]: number | string
  }
  co2: {
    [key: string]: number | string
  }
  innovations: {
    [key: string]: number | string
  }
  bom: Array<{
    component: string
    quantity: number
    unit_cost: number
    total_cost: number
  }>
  bom_cost: number
  suggested_cooling_class: string
}
