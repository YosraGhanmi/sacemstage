"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { Slider } from "@/components/ui/slider"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { BarChart3, Target, Zap, Save } from 'lucide-react'
import type { TransformerInputs, OptimizationVariant, OptimizationCriteria } from "@/lib/types"

interface OptimizationPanelProps {
  userInputs: TransformerInputs
}

export function OptimizationPanel({ userInputs }: OptimizationPanelProps) {
  const [criteria, setCriteria] = useState<OptimizationCriteria>({
    cost: true,
    efficiency: true,
    weight: false,
    losses: false,
  })
  const [numVariants, setNumVariants] = useState([5])
  const [variants, setVariants] = useState<OptimizationVariant[]>([])
  const [selectedVariant, setSelectedVariant] = useState<OptimizationVariant | null>(null)
  const [isOptimizing, setIsOptimizing] = useState(false)

  const handleOptimization = async () => {
    setIsOptimizing(true)

    try {
      // Simulate optimization process
      await new Promise((resolve) => setTimeout(resolve, 3000))

      // Generate mock variants
      const mockVariants: OptimizationVariant[] = Array.from({ length: numVariants[0] }, (_, i) => ({
        nom: `Variant ${i + 1}`,
        coût: 900 + Math.random() * 200,
        rendement: 95 + Math.random() * 2,
        poids: 170 + Math.random() * 30,
        pertes: 1000 + Math.random() * 300,
        score: Math.random() * 100,
        details: {
          b_max: 1.4 + Math.random() * 0.2,
          copper_mass: 40 + Math.random() * 10,
          core_type: ["Grain Oriented", "Amorphous", "Nanocrystalline"][Math.floor(Math.random() * 3)],
          cooling_class: ["ONAN", "ONAF", "OFAF"][Math.floor(Math.random() * 3)],
        },
      }))

      setVariants(mockVariants)
      setSelectedVariant(mockVariants[0])
    } catch (error) {
      console.error("Optimization error:", error)
    } finally {
      setIsOptimizing(false)
    }
  }

  const handleSaveVariant = async () => {
    if (!selectedVariant) return

    const payload = {
      nom: selectedVariant.nom,
      cout: selectedVariant.coût,
      rendement: selectedVariant.rendement,
      poids: selectedVariant.poids,
      pertes: selectedVariant.pertes,
      timestamp: new Date().toISOString(),
    }

    try {
      // Replace with your actual API endpoint
      const response = await fetch("/api/save-variant", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })

      if (response.ok) {
        alert("Variant saved successfully!")
      }
    } catch (error) {
      console.error("Save error:", error)
    }
  }

  return (
    <div className="space-y-6">
      {/* Optimization Setup */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Target className="h-5 w-5" />
            Multi-Criteria Optimization
          </CardTitle>
          <CardDescription>Configure optimization parameters and criteria for {userInputs.project}</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Criteria Selection */}
          <div>
            <h3 className="font-semibold mb-3">Optimization Criteria</h3>
            <div className="grid grid-cols-2 gap-4">
              {Object.entries(criteria).map(([key, checked]) => (
                <div key={key} className="flex items-center space-x-2">
                  <Checkbox
                    id={key}
                    checked={checked}
                    onCheckedChange={(checked) => setCriteria((prev) => ({ ...prev, [key]: !!checked }))}
                  />
                  <label htmlFor={key} className="capitalize font-medium">
                    {key === "cost"
                      ? "Cost"
                      : key === "efficiency"
                        ? "Efficiency"
                        : key === "weight"
                          ? "Weight"
                          : "Losses"}
                  </label>
                </div>
              ))}
            </div>
          </div>

          {/* Number of Variants */}
          <div>
            <h3 className="font-semibold mb-3">Number of Variants: {numVariants[0]}</h3>
            <Slider value={numVariants} onValueChange={setNumVariants} max={10} min={1} step={1} className="w-full" />
          </div>

          <Button onClick={handleOptimization} disabled={isOptimizing} className="w-full">
            {isOptimizing ? (
              <>
                <BarChart3 className="mr-2 h-4 w-4 animate-pulse" />
                Optimizing...
              </>
            ) : (
              <>
                <BarChart3 className="mr-2 h-4 w-4" />
                Generate Variants
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {/* Optimization Results */}
      {variants.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Zap className="h-5 w-5" />
              Optimization Results
            </CardTitle>
            <CardDescription>Generated variants ranked by optimization score</CardDescription>
          </CardHeader>
          <CardContent>
            {/* Variants Table */}
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Variant</TableHead>
                  <TableHead>Cost (€)</TableHead>
                  <TableHead>Efficiency (%)</TableHead>
                  <TableHead>Weight (kg)</TableHead>
                  <TableHead>Losses (W)</TableHead>
                  <TableHead>Score</TableHead>
                  <TableHead>Action</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {variants.map((variant, index) => (
                  <TableRow key={index} className={selectedVariant?.nom === variant.nom ? "bg-blue-50" : ""}>
                    <TableCell className="font-medium">{variant.nom}</TableCell>
                    <TableCell>{variant.coût.toFixed(2)}</TableCell>
                    <TableCell>{variant.rendement.toFixed(2)}</TableCell>
                    <TableCell>{variant.poids.toFixed(2)}</TableCell>
                    <TableCell>{variant.pertes.toFixed(0)}</TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <Progress value={variant.score} className="w-16" />
                        <span className="text-sm">{variant.score.toFixed(0)}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Button
                        variant={selectedVariant?.nom === variant.nom ? "default" : "outline"}
                        size="sm"
                        onClick={() => setSelectedVariant(variant)}
                      >
                        Select
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>

            {/* Selected Variant Details */}
            {selectedVariant && (
              <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                <h3 className="font-semibold mb-3">Selected Variant Details: {selectedVariant.nom}</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div>
                    <p className="text-sm text-gray-600">B Max</p>
                    <p className="font-semibold">{selectedVariant.details.b_max.toFixed(2)} T</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Copper Mass</p>
                    <p className="font-semibold">{selectedVariant.details.copper_mass.toFixed(2)} kg</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Core Type</p>
                    <Badge variant="secondary">{selectedVariant.details.core_type}</Badge>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Cooling Class</p>
                    <Badge variant="outline">{selectedVariant.details.cooling_class}</Badge>
                  </div>
                </div>

                <Button onClick={handleSaveVariant} className="mt-4 flex items-center gap-2">
                  <Save className="h-4 w-4" />
                  Save Variant
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  )
}
