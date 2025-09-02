"use client"

import type React from "react"
import { useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Loader2, Play, Upload, FileText } from "lucide-react"
import type { TransformerInputs } from "@/lib/types"

interface TransformerFormProps {
  onSubmit: (data: TransformerInputs) => void
  isCalculating: boolean
  mode: "calculation" | "optimization" | null
}

export function TransformerForm({ onSubmit, isCalculating, mode }: TransformerFormProps) {
  const [inputMethod, setInputMethod] = useState<"manual" | "file">("manual")
  const [formData, setFormData] = useState({
    // Informations générales
    nom_client: "",
    nom_projet: "",
    type_transformateur: "",
    type_installation: "",
    indice_horaire: "",

    // Paramètres de bobinage - Fixed variable names to match specification
    type_bob: "",
    epaisseur: "",
    hauteur: "",
    conducteur: "",
    etage: "",
    couche_bt: "",
    sps_bt: "", // Changed from spires_bt to sps_bt
    ep_papier: "", // Changed from epaisseur_papier to ep_papier
    nb_papier: "", // Changed from nombre_papier to nb_papier
    isolement_bt: "",
    nb_canaux_bt: "", // Changed from nombre_canaux_bt to nb_canaux_bt
    largeur_canal_bt: "",
    depart: "",
    dis_circuit_bt1: "", // Changed from distance_circuit_bt1 to dis_circuit_bt1

    // Spécifications électriques
    puissance_kva: "",
    tension_primaire: "",
    tension_secondaire: "",
    frequence_hz: "50",
    b_max: "1.5", // Changed from induction_max to b_max

    // Enroulements & circuit
    configuration: "",
    materiau_enroulement: "cuivre",
    couplage_primaire: "",
    couplage_secondaire: "",

    // Noyau magnétique
    materiau_noyau: "",
    type_tole: "",
    type_circuit_magnetique: "",

    // Refroidissement & température
    type_refroidissement: "",
    temperature: "",
    
  })

  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!mode) return

    const processedData: TransformerInputs = {
      ...formData,
      epaisseur: Number.parseFloat(formData.epaisseur) || 0,
      hauteur: Number.parseFloat(formData.hauteur) || 0,
      etage: Number.parseInt(formData.etage) || 0,
      couche_bt: Number.parseInt(formData.couche_bt) || 0,
      sps_bt: Number.parseInt(formData.sps_bt) || 0, // Updated field name
      ep_papier: Number.parseFloat(formData.ep_papier) || 0, // Updated field name
      nb_papier: Number.parseInt(formData.nb_papier) || 0, // Updated field name
      isolement_bt: Number.parseFloat(formData.isolement_bt) || 0,
      nb_canaux_bt: Number.parseInt(formData.nb_canaux_bt) || 0, // Updated field name
      largeur_canal_bt: Number.parseFloat(formData.largeur_canal_bt) || 0,
      dis_circuit_bt1: Number.parseFloat(formData.dis_circuit_bt1) || 0, // Updated field name
      puissance_kva: Number.parseFloat(formData.puissance_kva),
      tension_primaire: Number.parseFloat(formData.tension_primaire),
      tension_secondaire: Number.parseFloat(formData.tension_secondaire),
      frequence_hz: Number.parseFloat(formData.frequence_hz),
      b_max: Number.parseFloat(formData.b_max), // Updated field name
      temperature: Number.parseFloat(formData.temperature) || 0,
      indice_horaire: formData.indice_horaire|| "0",
      
    }

    onSubmit(processedData)
  }

  const updateField = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (e) => {
        try {
          const content = e.target?.result as string
          // Try to parse JSON file
          if (file.name.endsWith(".json")) {
            const data = JSON.parse(content)
            setFormData((prev) => ({ ...prev, ...data }))
          } else if (file.name.endsWith(".csv")) {
            // Basic CSV parsing - you can enhance this
            const lines = content.split("\n")
            const headers = lines[0].split(",")
            const values = lines[1].split(",")
            const data: Record<string, string> = {}
            headers.forEach((header, index) => {
              data[header.trim()] = values[index]?.trim() || ""
            })
            setFormData((prev) => ({ ...prev, ...data }))
          }
          setInputMethod("manual") // Switch to manual view to show loaded data
        } catch (error) {
          alert("Erreur lors de la lecture du fichier. Veuillez vérifier le format.")
        }
      }
      reader.readAsText(file)
    }
  }

  if (inputMethod === "file") {
    return (
      <div className="space-y-6">
        <div className="text-center">
          <FileText className="h-12 w-12 mx-auto mb-4 text-gray-400" />
          <h3 className="text-lg font-semibold mb-2">Importer un fichier</h3>
          <p className="text-sm text-gray-600 mb-4">
            Chargez un fichier JSON ou CSV contenant les paramètres du transformateur
          </p>

          <input ref={fileInputRef} type="file" accept=".json,.csv" onChange={handleFileUpload} className="hidden" />

          <Button onClick={() => fileInputRef.current?.click()} className="mb-4">
            <Upload className="mr-2 h-4 w-4" />
            Choisir un fichier
          </Button>

          <div className="text-xs text-gray-500 mb-4">Formats supportés: JSON, CSV</div>

          <Button variant="outline" onClick={() => setInputMethod("manual")} className="w-full">
            Ou saisir manuellement
          </Button>
        </div>
      </div>
    )
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Input Method Toggle */}
      <div className="flex gap-2 mb-4">
        <Button
          type="button"
          variant="outline"
          size="sm"
          onClick={() => setInputMethod("file")}
          className="flex items-center gap-2"
        >
          <Upload className="h-4 w-4" />
          Importer fichier
        </Button>
      </div>

      <div className="w-full">
        <Tabs defaultValue="general" className="w-full">
          <TabsList className="grid w-full grid-cols-5 mb-4">
            <TabsTrigger value="general" className="text-xs">
              Général
            </TabsTrigger>
            <TabsTrigger value="bobinage" className="text-xs">
              Bobinage
            </TabsTrigger>
            <TabsTrigger value="electrical" className="text-xs">
              Électrique
            </TabsTrigger>
            <TabsTrigger value="winding" className="text-xs">
              Enroulements
            </TabsTrigger>
            <TabsTrigger value="core" className="text-xs">
              Noyau
            </TabsTrigger>
          </TabsList>

          <TabsContent value="general" className="space-y-4 mt-4">
            <Card>
              <CardHeader>
                <CardTitle>Informations générales</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="nom_client">Nom du client *</Label>
                    <Input
                      id="nom_client"
                      value={formData.nom_client}
                      onChange={(e) => updateField("nom_client", e.target.value)}
                      placeholder="Nom du client"
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="nom_projet">Nom du projet *</Label>
                    <Input
                      id="nom_projet"
                      value={formData.nom_projet}
                      onChange={(e) => updateField("nom_projet", e.target.value)}
                      placeholder="Nom du projet"
                      required
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="type_transformateur">Type de transformateur</Label>
                    <Select
                      value={formData.type_transformateur}
                      onValueChange={(value) => updateField("type_transformateur", value)}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Sélectionner" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="hermetique">Hermétique</SelectItem>
                        <SelectItem value="respirant">Respirant</SelectItem>
                        <SelectItem value="H59">H59</SelectItem>
                        <SelectItem value="H61">H61</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="type_installation">Type d'installation</Label>
                    <Select
                      value={formData.type_installation}
                      onValueChange={(value) => updateField("type_installation", value)}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Sélectionner" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="exterieur">Extérieur</SelectItem>
                        <SelectItem value="poteau">Poteau</SelectItem>
                        <SelectItem value="interieur">Intérieur</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="bobinage" className="space-y-4 mt-4">
            <Card>
              <CardHeader>
                <CardTitle>Bobinage</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="type_bob">Type BOB</Label>
                    <Select value={formData.type_bob} onValueChange={(value) => updateField("type_bob", value)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Sélectionner" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="bande">Bande</SelectItem>
                        <SelectItem value="meplat">Méplat</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="epaisseur">Épaisseur</Label>
                    <Input
                      id="epaisseur"
                      type="number"
                      step="0.1"
                      value={formData.epaisseur}
                      onChange={(e) => updateField("epaisseur", e.target.value)}
                      placeholder="0.0"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="hauteur">Hauteur</Label>
                    <Input
                      id="hauteur"
                      type="number"
                      step="0.1"
                      value={formData.hauteur}
                      onChange={(e) => updateField("hauteur", e.target.value)}
                      placeholder="0.0"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="conducteur">Conducteur</Label>
                    <Input
                      id="conducteur"
                      value={formData.conducteur}
                      onChange={(e) => updateField("conducteur", e.target.value)}
                      placeholder="Conducteur"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="etage">Étage</Label>
                    <Input
                      id="etage"
                      type="number"
                      value={formData.etage}
                      onChange={(e) => updateField("etage", e.target.value)}
                      placeholder="0"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="couche_bt">Couche BT</Label>
                    <Input
                      id="couche_bt"
                      type="number"
                      value={formData.couche_bt}
                      onChange={(e) => updateField("couche_bt", e.target.value)}
                      placeholder="0"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="sps_bt">Spires BT</Label>
                    <Input
                      id="sps_bt"
                      type="number"
                      value={formData.sps_bt}
                      onChange={(e) => updateField("sps_bt", e.target.value)}
                      placeholder="0"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="ep_papier">Épaisseur Papier</Label>
                    <Input
                      id="ep_papier"
                      type="number"
                      step="0.1"
                      value={formData.ep_papier}
                      onChange={(e) => updateField("ep_papier", e.target.value)}
                      placeholder="0.0"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="nb_papier">Nombre Papier</Label>
                    <Input
                      id="nb_papier"
                      type="number"
                      value={formData.nb_papier}
                      onChange={(e) => updateField("nb_papier", e.target.value)}
                      placeholder="0"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="isolement_bt">Isolement BT</Label>
                    <Input
                      id="isolement_bt"
                      type="number"
                      step="0.1"
                      value={formData.isolement_bt}
                      onChange={(e) => updateField("isolement_bt", e.target.value)}
                      placeholder="0.0"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="nb_canaux_bt">Nombre Canaux BT</Label>
                    <Input
                      id="nb_canaux_bt"
                      type="number"
                      value={formData.nb_canaux_bt}
                      onChange={(e) => updateField("nb_canaux_bt", e.target.value)}
                      placeholder="0"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="largeur_canal_bt">Largeur Canal BT</Label>
                    <Input
                      id="largeur_canal_bt"
                      type="number"
                      step="0.1"
                      value={formData.largeur_canal_bt}
                      onChange={(e) => updateField("largeur_canal_bt", e.target.value)}
                      placeholder="0.0"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="depart">Départ</Label>
                    <Select value={formData.depart} onValueChange={(value) => updateField("depart", value)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Sélectionner" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="100">100</SelectItem>
                        <SelectItem value="90">90</SelectItem>
                        <SelectItem value="70">70</SelectItem>
                        <SelectItem value="50">50</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="dis_circuit_bt1">Distance Circuit BT1</Label>
                  <Input
                    id="dis_circuit_bt1"
                    type="number"
                    step="0.1"
                    value={formData.dis_circuit_bt1}
                    onChange={(e) => updateField("dis_circuit_bt1", e.target.value)}
                    placeholder="0.0"
                  />
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="electrical" className="space-y-4 mt-4">
            <Card>
              <CardHeader>
                <CardTitle>Spécifications électriques</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="puissance_kva">Puissance nominale (kVA) *</Label>
                    <Input
                      id="puissance_kva"
                      type="number"
                      value={formData.puissance_kva}
                      onChange={(e) => updateField("puissance_kva", e.target.value)}
                      placeholder="100"
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="frequence_hz">Fréquence (Hz)</Label>
                    <Select value={formData.frequence_hz} onValueChange={(value) => updateField("frequence_hz", value)}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="50">50 Hz</SelectItem>
                        <SelectItem value="60">60 Hz</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="tension_primaire">Tension primaire (V) *</Label>
                    <Input
                      id="tension_primaire"
                      type="number"
                      value={formData.tension_primaire}
                      onChange={(e) => updateField("tension_primaire", e.target.value)}
                      placeholder="20000"
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="tension_secondaire">Tension secondaire (V) *</Label>
                    <Input
                      id="tension_secondaire"
                      type="number"
                      value={formData.tension_secondaire}
                      onChange={(e) => updateField("tension_secondaire", e.target.value)}
                      placeholder="400"
                      required
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="b_max">Induction magnétique max (B_max en T)</Label>
                  <Input
                    id="b_max"
                    type="number"
                    step="0.1"
                    value={formData.b_max}
                    onChange={(e) => updateField("b_max", e.target.value)}
                    placeholder="1.5"
                  />
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="winding" className="space-y-4 mt-4">
            <Card>
              <CardHeader>
                <CardTitle>Enroulements & circuit</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="configuration">Configuration</Label>
                    <Select
                      value={formData.configuration}
                      onValueChange={(value) => updateField("configuration", value)}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Sélectionner" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="triphase">Triphasé</SelectItem>
                        <SelectItem value="monophase">Monophasé</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="materiau_enroulement">Matériau des enroulements</Label>
                    <Select
                      value={formData.materiau_enroulement}
                      onValueChange={(value) => updateField("materiau_enroulement", value)}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="cuivre">Cuivre</SelectItem>
                        <SelectItem value="aluminium">Aluminium</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="couplage_primaire">Couplage primaire</Label>
                    <Select
                      value={formData.couplage_primaire}
                      onValueChange={(value) => updateField("couplage_primaire", value)}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Sélectionner" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="D">D</SelectItem>
                        <SelectItem value="YN">YN</SelectItem>
                        <SelectItem value="Y">Y</SelectItem>
                        <SelectItem value="ZN">ZN</SelectItem>
                        <SelectItem value="Z">Z</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="couplage_secondaire">Couplage secondaire</Label>
                    <Select
                      value={formData.couplage_secondaire}
                      onValueChange={(value) => updateField("couplage_secondaire", value)}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Sélectionner" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="YN">YN</SelectItem>
                        <SelectItem value="D">D</SelectItem>
                        <SelectItem value="Y">Y</SelectItem>
                        <SelectItem value="ZN">ZN</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="indice_horaire">Indice horaire</Label>
                  <Select
                    value={formData.indice_horaire}
                    onValueChange={(value) => updateField("indice_horaire", value)}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Sélectionner" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="0">0</SelectItem>
                      <SelectItem value="1">1</SelectItem>
                      <SelectItem value="2">2</SelectItem>
                      <SelectItem value="3">3</SelectItem>
                      <SelectItem value="4">4</SelectItem>
                      <SelectItem value="5">5</SelectItem>
                      <SelectItem value="6">6</SelectItem>
                      <SelectItem value="7">7</SelectItem>
                      <SelectItem value="8">8</SelectItem>
                      <SelectItem value="9">9</SelectItem>
                      <SelectItem value="10">10</SelectItem>
                      <SelectItem value="11">11</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="core" className="space-y-4 mt-4">
            <Card>
              <CardHeader>
                <CardTitle>Noyau magnétique & Refroidissement</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="materiau_noyau">Matériau du noyau</Label>
                    <Select
                      value={formData.materiau_noyau}
                      onValueChange={(value) => updateField("materiau_noyau", value)}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Sélectionner" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="acier_electrique">Acier électrique</SelectItem>
                        <SelectItem value="acier_hib">Acier HiB</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="type_tole">Type de tôle</Label>
                    <Select value={formData.type_tole} onValueChange={(value) => updateField("type_tole", value)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Sélectionner" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="M110-23">M110-23</SelectItem>
                        <SelectItem value="M120-27">M120-27</SelectItem>
                        <SelectItem value="M130-30">M130-30</SelectItem>
                        <SelectItem value="H75-23">H75-23</SelectItem>
                        <SelectItem value="H85-23">H85-23</SelectItem>
                        <SelectItem value="H80-23">H80-23</SelectItem>
                        <SelectItem value="H95-27">H95-27</SelectItem>
                        <SelectItem value="H105-30">H105-30</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="type_circuit_magnetique">Type de circuit magnétique</Label>
                    <Select
                      value={formData.type_circuit_magnetique}
                      onValueChange={(value) => updateField("type_circuit_magnetique", value)}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Sélectionner" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="3colonnes">3 Colonnes</SelectItem>
                        <SelectItem value="4colonnes">4 Colonnes</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="type_refroidissement">Type de refroidissement</Label>
                    <Select
                      value={formData.type_refroidissement}
                      onValueChange={(value) => updateField("type_refroidissement", value)}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Sélectionner" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="ONAN">ONAN</SelectItem>
                        <SelectItem value="ONAF">ONAF</SelectItem>
                        <SelectItem value="ONAN+">ONAN+</SelectItem>
                        <SelectItem value="AN">AN</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="temperature">température (°C)</Label>
                  <Input
                    id="temperature"
                    type="number"
                    value={formData.temperature}
                    onChange={(e) => updateField("temperature", e.target.value)}
                    placeholder="65"
                  />
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>

      <Button type="submit" className="w-full" disabled={isCalculating || !mode}>
        {isCalculating ? (
          <>
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            Calcul en cours...
          </>
        ) : (
          <>
            <Play className="mr-2 h-4 w-4" />
            {mode === "calculation" ? "Lancer le calcul" : "Démarrer l'optimisation"}
          </>
        )}
      </Button>
    </form>
  )
}
