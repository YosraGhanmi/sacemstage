import { type NextRequest, NextResponse } from "next/server"
import { exec } from "child_process"
import { promisify } from "util"

const execAsync = promisify(exec)

export async function POST(request: NextRequest) {
  try {
    const data = await request.json()

    if (!data.inputs || !data.optimization_objectives) {
      return NextResponse.json(
        { error: "Missing required parameters: inputs and optimization_objectives" },
        { status: 400 },
      )
    }

    const optimizationData = {
      ...data.inputs,
      optimization_mode: true,
      optimization_objectives: data.optimization_objectives,
      optimization_constraints: data.optimization_constraints || {},
      algorithm: data.algorithm || "multi_objective",
    }

    const { stdout, stderr } = await execAsync(`python scripts/transformer_calculator.py`, {
      env: {
        ...process.env,
        ENTREES_JSON: JSON.stringify(optimizationData),
      },
    })

    if (stderr) {
      console.error("Optimization error:", stderr)
      throw new Error(`Optimization failed: ${stderr}`)
    }

    const results = JSON.parse(stdout.trim())

    return NextResponse.json({
      success: true,
      optimization_results: results,
      pareto_front: results.pareto_front || [],
      best_solutions: results.best_solutions || [],
    })
  } catch (error) {
    console.error("Optimization API Error:", error)
    return NextResponse.json(
      {
        success: false,
        error: "Optimization failed",
        details: error instanceof Error ? error.message : String(error),
      },
      { status: 500 },
    )
  }
}
