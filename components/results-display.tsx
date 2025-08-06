"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Progress } from "@/components/ui/progress"
import { Zap, CogIcon as Coil, Magnet, Thermometer, Wrench, TrendingDown, Lightbulb, Package, Download, Send } from 'lucide-react'
import type { TransformerResults, TransformerInputs, BOMItem } from "@/lib/types"

interface ResultsDisplayProps {
  results: TransformerResults
  userInputs: TransformerInputs
}

export function ResultsDisplay({ results, userInputs }: ResultsDisplayProps) {
  const handleApiSend = async () => {
    const apiData = {
      installation: userInputs.installation_type,
      type: userInputs.transformer_type,
      client: userInputs.client_name,
      project_name: userInputs.project_name,
      copper_mass_kg: results.copper_mass_kg,
      efficiency: results.improved_efficiency_percent,
      cost_15y: results.lifetime_cost_eur,
      losses_total: results.thermal.losses_total_W,
      power_kva: userInputs.power_kva,
      secondary_voltage: userInputs.secondary_voltage,
      primary_voltage: userInputs.primary_voltage,
      transformer_type: userInputs.transformer_type,
      winding_material: userInputs.winding_material,
      b_max: userInputs.b_max,
    }

    try {
      // Replace with your actual API endpoint
      const response = await fetch("/api/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(apiData),
      })

      if (response.ok) {
        alert("Data sent successfully!")
      }
    } catch (error) {
      console.error("API Error:", error)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Zap className="h-5 w-5" />
          Calculation Results
        </CardTitle>
        <CardDescription>Comprehensive transformer analysis and specifications</CardDescription>
      </CardHeader>
      <CardContent>
        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Copper Mass</p>
                  <p className="text-2xl font-bold">{results.copper_mass_kg.toFixed(2)} kg</p>
                </div>
                <Coil className="h-8 w-8 text-orange-500" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Efficiency</p>
                  <p className="text-2xl font-bold">{results.improved_efficiency_percent}%</p>
                </div>
                <TrendingDown className="h-8 w-8 text-green-500" />
              </div>
              <Progress value={results.improved_efficiency_percent} className="mt-2" />
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">15-Year Cost</p>
                  <p className="text-2xl font-bold">€{results.lifetime_cost_eur.toLocaleString()}</p>
                </div>
                <Package className="h-8 w-8 text-blue-500" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Detailed Results Tabs */}
        <Tabs defaultValue="electrical" className="w-full">
          <TabsList className="grid w-full grid-cols-4 lg:grid-cols-8">
            <TabsTrigger value="electrical" className="flex items-center gap-1">
              <Zap className="h-4 w-4" />
              <span className="hidden sm:inline">Electrical</span>
            </TabsTrigger>
            <TabsTrigger value="winding" className="flex items-center gap-1">
              <Coil className="h-4 w-4" />
              <span className="hidden sm:inline">Winding</span>
            </TabsTrigger>
            <TabsTrigger value="magnetic" className="flex items-center gap-1">
              <Magnet className="h-4 w-4" />
              <span className="hidden sm:inline">Magnetic</span>
            </TabsTrigger>
            <TabsTrigger value="thermal" className="flex items-center gap-1">
              <Thermometer className="h-4 w-4" />
              <span className="hidden sm:inline">Thermal</span>
            </TabsTrigger>
            <TabsTrigger value="mechanical" className="flex items-center gap-1">
              <Wrench className="h-4 w-4" />
              <span className="hidden sm:inline">Mechanical</span>
            </TabsTrigger>
            <TabsTrigger value="losses" className="flex items-center gap-1">
              <TrendingDown className="h-4 w-4" />
              <span className="hidden sm:inline">Losses</span>
            </TabsTrigger>
            <TabsTrigger value="innovative" className="flex items-center gap-1">
              <Lightbulb className="h-4 w-4" />
              <span className="hidden sm:inline">Innovation</span>
            </TabsTrigger>
            <TabsTrigger value="bom" className="flex items-center gap-1">
              <Package className="h-4 w-4" />
              <span className="hidden sm:inline">BOM</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="electrical" className="mt-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Zap className="h-5 w-5" />
                  Electrical Calculations
                </CardTitle>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Parameter</TableHead>
                      <TableHead>Value</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {Object.entries(results.electrical).map(([key, value]) => (
                      <TableRow key={key}>
                        <TableCell className="font-medium">{key}</TableCell>
                        <TableCell>{typeof value === "number" ? value.toFixed(2) : String(value)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="winding" className="mt-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Coil className="h-5 w-5" />
                  Winding Calculations
                </CardTitle>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Parameter</TableHead>
                      <TableHead>Value</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {Object.entries(results.winding).map(([key, value]) => (
                      <TableRow key={key}>
                        <TableCell className="font-medium">{key}</TableCell>
                        <TableCell>{typeof value === "number" ? value.toFixed(2) : String(value)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="magnetic" className="mt-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Magnet className="h-5 w-5" />
                  Magnetic Calculations
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                    <span className="font-medium">Core Weight</span>
                    <Badge variant="secondary">{results.geometry.core_weight_kg.toFixed(2)} kg</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="thermal" className="mt-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Thermometer className="h-5 w-5" />
                  Thermal Analysis
                </CardTitle>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Parameter</TableHead>
                      <TableHead>Value</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {Object.entries(results.thermal).map(([key, value]) => (
                      <TableRow key={key}>
                        <TableCell className="font-medium">{key}</TableCell>
                        <TableCell>{typeof value === "number" ? value.toFixed(2) : String(value)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="mechanical" className="mt-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Wrench className="h-5 w-5" />
                  Mechanical Properties
                </CardTitle>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Parameter</TableHead>
                      <TableHead>Value</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {Object.entries(results.mechanical).map(([key, value]) => (
                      <TableRow key={key}>
                        <TableCell className="font-medium">{key}</TableCell>
                        <TableCell>{typeof value === "number" ? value.toFixed(2) : String(value)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="losses" className="mt-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingDown className="h-5 w-5" />
                  Loss Analysis
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="p-4 bg-red-50 rounded-lg">
                      <p className="text-sm text-red-600">Copper Losses</p>
                      <p className="text-xl font-bold text-red-700">{results.electrical.losses_copper_W} W</p>
                    </div>
                    <div className="p-4 bg-orange-50 rounded-lg">
                      <p className="text-sm text-orange-600">Core Losses</p>
                      <p className="text-xl font-bold text-orange-700">{results.electrical.losses_core_W} W</p>
                    </div>
                    <div className="p-4 bg-gray-50 rounded-lg">
                      <p className="text-sm text-gray-600">Total Losses</p>
                      <p className="text-xl font-bold text-gray-700">{results.thermal.losses_total_W} W</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="innovative" className="mt-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Lightbulb className="h-5 w-5" />
                  Innovation Metrics
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="p-4 bg-green-50 rounded-lg">
                      <p className="text-sm text-green-600">CO2 Footprint</p>
                      <p className="text-xl font-bold text-green-700">
                        {results.co2["Empreinte carbone (kg CO2)"]} kg CO2
                      </p>
                    </div>
                    <div className="p-4 bg-blue-50 rounded-lg">
                      <p className="text-sm text-blue-600">Recyclability</p>
                      <p className="text-xl font-bold text-blue-700">{results.co2["Recyclabilité (%)"]}%</p>
                    </div>
                  </div>

                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Innovation Metric</TableHead>
                        <TableHead>Value</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {Object.entries(results.innovations).map(([key, value]) => (
                        <TableRow key={key}>
                          <TableCell className="font-medium">{key}</TableCell>
                          <TableCell>{typeof value === "number" ? value.toFixed(2) : String(value)}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="bom" className="mt-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Package className="h-5 w-5" />
                  Bill of Materials
                </CardTitle>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Component</TableHead>
                      <TableHead>Quantity</TableHead>
                      <TableHead>Unit Cost (€)</TableHead>
                      <TableHead>Total Cost (€)</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {results.bom.map((item: BOMItem, index: number) => (
                      <TableRow key={index}>
                        <TableCell className="font-medium">{item.component}</TableCell>
                        <TableCell>{item.quantity}</TableCell>
                        <TableCell>{item.unit_cost.toFixed(2)}</TableCell>
                        <TableCell>{item.total_cost.toFixed(2)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
                <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold">Total BOM Cost:</span>
                    <Badge variant="default" className="text-lg px-3 py-1">
                      €{results.bom_cost.toFixed(2)}
                    </Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Action Buttons */}
        <div className="flex gap-4 mt-6">
          <Button onClick={handleApiSend} className="flex items-center gap-2">
            <Send className="h-4 w-4" />
            Send to API
          </Button>
          <Button variant="outline" className="flex items-center gap-2 bg-transparent">
            <Download className="h-4 w-4" />
            Download PDF Report
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
