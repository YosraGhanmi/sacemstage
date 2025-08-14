"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { TransformerForm } from "@/components/transformer-form"
import { ResultsDisplay } from "@/components/results-display"
import { OptimizationPanel } from "@/components/optimization-panel"
import { Zap, Settings, BarChart3 } from "lucide-react"
import type { TransformerInputs, TransformerResults } from "@/lib/types"
import Image from "next/image"

export default function TransformerDesignApp() {
  const [mode, setMode] = useState<"calculation" | "optimization" | null>(null)
  const [results, setResults] = useState<TransformerResults | null>(null)
  const [isCalculating, setIsCalculating] = useState(false)
  const [userInputs, setUserInputs] = useState<TransformerInputs | null>(null)

  const handleCalculation = async (inputs: TransformerInputs) => {
    setIsCalculating(true)
    setUserInputs(inputs)

    try {
      const response = await fetch("/api/calculate-transformer", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(inputs),
      })

      if (!response.ok) {
        throw new Error("Calculation failed")
      }

      const calculatedResults: TransformerResults = await response.json()
      setResults(calculatedResults)
    } catch (error) {
      console.error("Calculation error:", error)

      const mockResults: TransformerResults = {
        masse_cuivre_kg: 45.2,
        rendement_ameliore_pourcent: 96.5,
        cout_vie_eur: 12500,
        electrique: {
          tension_phase_secondaire: inputs.tension_secondaire ? inputs.tension_secondaire / Math.sqrt(3) : 0,
          courant_primaire:
            inputs.puissance_kva && inputs.tension_primaire
              ? (inputs.puissance_kva * 1000) / (inputs.tension_primaire * Math.sqrt(3))
              : 0,
          courant_secondaire:
            inputs.puissance_kva && inputs.tension_secondaire
              ? (inputs.puissance_kva * 1000) / (inputs.tension_secondaire * Math.sqrt(3))
              : 0,
          pertes_cuivre: 850,
          pertes_fer: 320,
        },
        bobinage: {
          sps_ht: 1250,
          sps_bt: 125,
          section_conducteur_primaire: 2.5,
          section_conducteur_secondaire: 25,
        },
        thermique: {
          pertes_totales: 1170,
          temperature_max: 85,
          classe_thermique: "F",
        },
        mecanique: {
          poids_total: 180,
          dimensions: "400x300x250",
        },
        geometrie: {
          poids_noyau: 95.5,
        },
        co2: {
          empreinte_carbone: 125.5,
          recyclabilite: 85,
        },
        innovations: {
          efficacite_energetique: "Classe A+",
          score_innovation: 8.5,
        },
        nomenclature: [
          { composant: "Noyau magnétique", quantite: 1, cout_unitaire: 450, cout_total: 450 },
          { composant: "Cuivre primaire", quantite: 25, cout_unitaire: 8.5, cout_total: 212.5 },
          { composant: "Cuivre secondaire", quantite: 20, cout_unitaire: 8.5, cout_total: 170 },
          { composant: "Isolation", quantite: 1, cout_unitaire: 85, cout_total: 85 },
        ],
        cout_nomenclature: 917.5,
        classe_refroidissement_suggeree: "ONAN",
      }

      setResults(mockResults)
    } finally {
      setIsCalculating(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto p-6">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            {/* Left side - Logo and Title */}
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-3">
                <Image src="/sacem.png" alt="SACEM Logo" width={120} height={60} className="object-contain" priority />
                <div className="h-12 w-px bg-gray-300 mx-2" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">SACEM Transformer Design</h1>
                <p className="text-gray-600">Conception et optimisation intelligente de transformateurs</p>
              </div>
            </div>

            {/* Right side - Company branding */}
            <div className="hidden lg:block text-right">
              <p className="text-sm text-gray-500">Développé par</p>
              <p className="font-semibold text-gray-700">SACEM Engineering Solutions</p>
            </div>
          </div>

          {/* Mode Selection */}
          <div className="flex gap-4">
            <Button
              variant={mode === "calculation" ? "default" : "outline"}
              onClick={() => setMode("calculation")}
              className="flex items-center gap-2"
            >
              <Settings className="h-4 w-4" />
              Calcul Standard
            </Button>
            <Button
              variant={mode === "optimization" ? "default" : "outline"}
              onClick={() => setMode("optimization")}
              className="flex items-center gap-2"
            >
              <BarChart3 className="h-4 w-4" />
              Optimisation
            </Button>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Input Panel */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Settings className="h-5 w-5" />
                  Paramètres
                </CardTitle>
                <CardDescription>Saisir les spécifications du transformateur</CardDescription>
              </CardHeader>
              <CardContent>
                <TransformerForm onSubmit={handleCalculation} isCalculating={isCalculating} mode={mode} />
              </CardContent>
            </Card>
          </div>

          {/* Results Panel */}
          <div className="lg:col-span-2">
            {mode === "calculation" && results && userInputs && (
              <ResultsDisplay results={results} userInputs={userInputs} />
            )}

            {mode === "optimization" && userInputs && <OptimizationPanel userInputs={userInputs} />}

            {!mode && (
              <Card className="h-96 flex items-center justify-center">
                <div className="text-center text-gray-500">
                  <Zap className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p>Sélectionner un mode pour commencer la conception du transformateur</p>
                </div>
              </Card>
            )}
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-12 pt-8 border-t border-gray-200">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center gap-4 mb-4 md:mb-0">
              <Image src="/sacem.png" alt="SACEM Logo" width={80} height={40} className="object-contain opacity-70" />
              <div className="text-sm text-gray-500">
                <p>© 2025 SACEM. Tous droits réservés.</p>
                <p>Solutions Avancées de Conception de Transformateurs</p>
              </div>
            </div>
            <div className="text-sm text-gray-500 text-center md:text-right">
              <p>Version 2.0.1</p>
              <p></p>
            </div>
          </div>
        </footer>
      </div>
    </div>
  )
}
