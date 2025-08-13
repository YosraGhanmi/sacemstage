"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Download, Zap, Cog, Leaf } from "lucide-react"
import type { TransformerInputs, TransformerResults } from "@/lib/types"

interface ResultsDisplayProps {
  results: TransformerResults
  userInputs: TransformerInputs
}

export function ResultsDisplay({ results, userInputs }: ResultsDisplayProps) {
  const handleDownloadPDF = async () => {
    try {
      const response = await fetch("/api/generate-pdf", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ inputs: userInputs, results }),
      })

      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement("a")
        a.style.display = "none"
        a.href = url
        a.download = `transformer_${userInputs.project_name || "calculation"}.pdf`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
      } else {
        alert("Error generating PDF")
      }
    } catch (error) {
      console.error("PDF generation error:", error)
      alert("Error generating PDF")
    }
  }

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Efficiency</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{results.improved_efficiency_percent}%</div>
            <p className="text-xs text-muted-foreground">Energy efficiency rating</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Copper Mass</CardTitle>
            <Cog className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{results.copper_mass_kg} kg</div>
            <p className="text-xs text-muted-foreground">Total copper weight</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Lifetime Cost</CardTitle>
            <Leaf className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">€{results.lifetime_cost_eur.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">20-year total cost</p>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Results */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Calculation Results</CardTitle>
              <CardDescription>Complete transformer design calculations for {userInputs.project_name}</CardDescription>
            </div>
            <Button onClick={handleDownloadPDF} className="flex items-center gap-2">
              <Download className="h-4 w-4" />
              Download PDF
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="electrical" className="w-full">
            <TabsList className="grid w-full grid-cols-6">
              <TabsTrigger value="electrical">Electrical</TabsTrigger>
              <TabsTrigger value="winding">Winding</TabsTrigger>
              <TabsTrigger value="thermal">Thermal</TabsTrigger>
              <TabsTrigger value="mechanical">Mechanical</TabsTrigger>
              <TabsTrigger value="bom">BOM</TabsTrigger>
              <TabsTrigger value="environmental">Environmental</TabsTrigger>
            </TabsList>

            <TabsContent value="electrical" className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                {Object.entries(results.electrical).map(([key, value]) => (
                  <div key={key} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                    <span className="text-sm font-medium">{key}</span>
                    <Badge variant="secondary">{typeof value === "number" ? value.toFixed(2) : value}</Badge>
                  </div>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="winding" className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                {Object.entries(results.winding).map(([key, value]) => (
                  <div key={key} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                    <span className="text-sm font-medium">{key}</span>
                    <Badge variant="secondary">{typeof value === "number" ? value.toFixed(2) : value}</Badge>
                  </div>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="thermal" className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                {Object.entries(results.thermal).map(([key, value]) => (
                  <div key={key} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                    <span className="text-sm font-medium">{key}</span>
                    <Badge variant="secondary">{typeof value === "number" ? value.toFixed(2) : value}</Badge>
                  </div>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="mechanical" className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                {Object.entries(results.mechanical).map(([key, value]) => (
                  <div key={key} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                    <span className="text-sm font-medium">{key}</span>
                    <Badge variant="secondary">{typeof value === "number" ? value.toFixed(2) : value}</Badge>
                  </div>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="bom" className="space-y-4">
              <div className="space-y-3">
                {results.bom.map((item, index) => (
                  <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                    <div>
                      <span className="font-medium">{item.component}</span>
                      <span className="text-sm text-gray-500 ml-2">({item.quantity} units)</span>
                    </div>
                    <div className="text-right">
                      <div className="font-medium">€{item.total_cost.toFixed(2)}</div>
                      <div className="text-sm text-gray-500">€{item.unit_cost.toFixed(2)}/unit</div>
                    </div>
                  </div>
                ))}
                <Separator />
                <div className="flex justify-between items-center p-3 bg-blue-50 rounded font-bold">
                  <span>Total BOM Cost</span>
                  <span>€{results.bom_cost.toFixed(2)}</span>
                </div>
              </div>
            </TabsContent>

            <TabsContent value="environmental" className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                {Object.entries(results.co2).map(([key, value]) => (
                  <div key={key} className="flex justify-between items-center p-3 bg-green-50 rounded">
                    <span className="text-sm font-medium">{key}</span>
                    <Badge variant="secondary">{typeof value === "number" ? value.toFixed(2) : value}</Badge>
                  </div>
                ))}
                <div className="col-span-2">
                  <div className="flex justify-between items-center p-3 bg-blue-50 rounded">
                    <span className="text-sm font-medium">Suggested Cooling Class</span>
                    <Badge variant="default">{results.suggested_cooling_class}</Badge>
                  </div>
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  )
}
