"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { TransformerForm } from "@/components/transformer-form"
import { ResultsDisplay } from "@/components/results-display"
import { OptimizationPanel } from "@/components/optimization-panel"
import { Zap, Settings, BarChart3 } from 'lucide-react'
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
      // Simulate API call - replace with actual calculation logic
      await new Promise((resolve) => setTimeout(resolve, 2000))

      // Mock results based on your Python structure
      const mockResults: TransformerResults = {
        copper_mass_kg: 45.2,
        improved_efficiency_percent: 96.5,
        lifetime_cost_eur: 12500,
        electrical: {
          "Tension secondaire phase (V)": inputs.secondary_voltage / Math.sqrt(3),
          "Courant primaire (A)": (inputs.power_kva * 1000) / (inputs.primary_voltage * Math.sqrt(3)),
          "Courant secondaire (A)": (inputs.power_kva * 1000) / (inputs.secondary_voltage * Math.sqrt(3)),
          losses_copper_W: 850,
          losses_core_W: 320,
        },
        winding: {
          "Nombre de spires primaire": 1250,
          "Nombre de spires secondaire": 125,
          "Section conducteur primaire (mm²)": 2.5,
          "Section conducteur secondaire (mm²)": 25,
        },
        thermal: {
          losses_total_W: 1170,
          "Température max (°C)": 85,
          "Classe thermique": "F",
        },
        mechanical: {
          "Poids total (kg)": 180,
          "Dimensions (mm)": "400x300x250",
        },
        geometry: {
          core_weight_kg: 95.5,
        },
        co2: {
          "Empreinte carbone (kg CO2)": 125.5,
          "Recyclabilité (%)": 85,
        },
        innovations: {
          "Efficacité énergétique": "Classe A+",
          "Innovation score": 8.5,
        },
        bom: [
          { component: "Noyau magnétique", quantity: 1, unit_cost: 450, total_cost: 450 },
          { component: "Cuivre primaire", quantity: 25, unit_cost: 8.5, total_cost: 212.5 },
          { component: "Cuivre secondaire", quantity: 20, unit_cost: 8.5, total_cost: 170 },
          { component: "Isolation", quantity: 1, unit_cost: 85, total_cost: 85 },
        ],
        bom_cost: 917.5,
        suggested_cooling_class: "ONAN",
      }

      setResults(mockResults)
    } catch (error) {
      console.error("Calculation error:", error)
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
                <Image
                  src="/sacem.png"
                  alt="SACEM Logo"
                  width={120}
                  height={60}
                  className="object-contain"
                  priority
                />
                <div className="h-12 w-px bg-gray-300 mx-2" />
                
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">SACEM Transformer Design</h1>
                <p className="text-gray-600">Intelligent transformer conception and optimization</p>
              </div>
            </div>

            {/* Right side - Company branding */}
            <div className="hidden lg:block text-right">
              <p className="text-sm text-gray-500">Powered by</p>
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
              Standard Calculation
            </Button>
            <Button
              variant={mode === "optimization" ? "default" : "outline"}
              onClick={() => setMode("optimization")}
              className="flex items-center gap-2"
            >
              <BarChart3 className="h-4 w-4" />
              Optimization
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
                  Parameters
                </CardTitle>
                <CardDescription>Enter transformer specifications</CardDescription>
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
                  <p>Select a mode to begin transformer design</p>
                </div>
              </Card>
            )}
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-12 pt-8 border-t border-gray-200">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center gap-4 mb-4 md:mb-0">
              <Image
                src="/sacem.png"
                alt="SACEM Logo"
                width={80}
                height={40}
                className="object-contain opacity-70"
              />
              <div className="text-sm text-gray-500">
                <p>© 2025 SACEM. All rights reserved.</p>
                <p>Advanced Transformer Design Solutions</p>
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
