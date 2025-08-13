import { type NextRequest, NextResponse } from "next/server"
import { TransformerCalculator } from "@/lib/transformer-calculator"
import { PDFFieldMapper } from "@/lib/pdf-field-mapper"
import type { TransformerInputs } from "@/lib/types"

export async function POST(request: NextRequest) {
  try {
    const inputs: TransformerInputs = await request.json()

    // Validate required inputs
    if (!inputs.power_kva || !inputs.primary_voltage || !inputs.secondary_voltage) {
      return NextResponse.json(
        { error: "Missing required parameters: power_kva, primary_voltage, secondary_voltage" },
        { status: 400 },
      )
    }

    // Initialize calculator
    const calculator = new TransformerCalculator(inputs)

    // Perform all calculations
    const results = calculator.calculateAll()

    // Generate PDF field mapping
    const mapper = new PDFFieldMapper()
    const pdfData = mapper.mapToPDFFields(inputs, results)

    // Return results with PDF mapping
    return NextResponse.json({
      ...results,
      pdfFieldMapping: pdfData,
    })
  } catch (error) {
    console.error("Calculation error:", error)
    return NextResponse.json({ error: "Internal calculation error" }, { status: 500 })
  }
}
