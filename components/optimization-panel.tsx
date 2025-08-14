"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { BarChart3, TrendingUp, Zap } from "lucide-react"
import type { TransformerInputs } from "@/lib/types"

interface OptimizationPanelProps {
  userInputs: TransformerInputs
}

export function OptimizationPanel({ userInputs }: OptimizationPanelProps) {
  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="h-5 w-5" />
            Optimization Analysis
          </CardTitle>
          <CardDescription>Multi-objective optimization for {userInputs.nom_projet}</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {/* Optimization Progress */}
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium">Cost Optimization</span>
                <span className="text-sm text-muted-foreground">85%</span>
              </div>
              <Progress value={85} className="w-full" />
            </div>

            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium">Efficiency Optimization</span>
                <span className="text-sm text-muted-foreground">92%</span>
              </div>
              <Progress value={92} className="w-full" />
            </div>

            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium">Weight Optimization</span>
                <span className="text-sm text-muted-foreground">78%</span>
              </div>
              <Progress value={78} className="w-full" />
            </div>

            {/* Optimization Results */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm">Cost Reduction</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-green-600">-15%</div>
                  <p className="text-xs text-muted-foreground">vs standard design</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm">Efficiency Gain</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-blue-600">+2.3%</div>
                  <p className="text-xs text-muted-foreground">improved performance</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm">Weight Reduction</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-purple-600">-8kg</div>
                  <p className="text-xs text-muted-foreground">lighter design</p>
                </CardContent>
              </Card>
            </div>

            {/* Recommendations */}
            <div className="space-y-3 mt-6">
              <h4 className="font-medium">Optimization Recommendations</h4>
              <div className="space-y-2">
                <div className="flex items-center gap-2 p-2 bg-green-50 rounded">
                  <TrendingUp className="h-4 w-4 text-green-600" />
                  <span className="text-sm">Use {userInputs.type_tole || "H85-23"} steel for better efficiency</span>
                  <Badge variant="secondary" className="ml-auto">
                    +1.2%
                  </Badge>
                </div>
                <div className="flex items-center gap-2 p-2 bg-blue-50 rounded">
                  <Zap className="h-4 w-4 text-blue-600" />
                  <span className="text-sm">Optimize conductor cross-section</span>
                  <Badge variant="secondary" className="ml-auto">
                    -€250
                  </Badge>
                </div>
                <div className="flex items-center gap-2 p-2 bg-purple-50 rounded">
                  <BarChart3 className="h-4 w-4 text-purple-600" />
                  <span className="text-sm">
                    Consider {userInputs.type_refroidissement || "ONAN"} cooling for this power rating
                  </span>
                  <Badge variant="secondary" className="ml-auto">
                    Optimal
                  </Badge>
                </div>
              </div>
            </div>

            <Button className="w-full mt-6">Apply Optimized Design</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
