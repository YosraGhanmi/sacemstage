export interface TransformerInputs {
  // Informations générales
  nom_client: string
  nom_projet: string
  type_transformateur: string
  type_installation: string

  // Paramètres de bobinage
  type_bob: string
  epaisseur: number
  hauteur: number
  conducteur: string
  etage: number
  couche_bt: number
  sps_bt: number
  ep_papier: number
  nb_papier: number
  isolement_bt: number
  nb_canaux_bt: number
  largeur_canal_bt: number
  depart: string
  dis_circuit_bt1: number

  // Spécifications électriques
  puissance_kva: number
  tension_primaire: number
  tension_secondaire: number
  frequence_hz: number
  b_max: number

  // Enroulements et circuit
  configuration: string
  materiau_enroulement: string
  couplage_primaire: string
  couplage_secondaire: string

  // Noyau et refroidissement
  materiau_noyau: string
  type_tole: string
  type_circuit_magnetique: string
  type_refroidissement: string
  elevation_temperature_max: number
}

export interface TransformerResults {
  masse_cuivre_kg: number
  rendement_ameliore_pourcent: number
  cout_vie_eur: number
  electrique: {
    [key: string]: number | string
  }
  bobinage: {
    [key: string]: number | string
  }
  thermique: {
    [key: string]: number | string
  }
  mecanique: {
    [key: string]: number | string
  }
  geometrie: {
    [key: string]: number | string
  }
  co2: {
    [key: string]: number | string
  }
  innovations: {
    [key: string]: number | string
  }
  nomenclature: Array<{
    composant: string
    quantite: number
    cout_unitaire: number
    cout_total: number
  }>
  cout_nomenclature: number
  classe_refroidissement_suggeree: string
}
