import { type NextRequest, NextResponse } from "next/server"
import { exec } from "child_process"
import { promisify } from "util"
import fs from "fs"
import path from "path"
import { PDFFieldMapper } from "@/lib/pdf-field-mapper"
import type { TransformerInputs, TransformerResults } from "@/lib/types"

const execAsync = promisify(exec)

export async function POST(request: NextRequest) {
  try {
    console.log("Starting PDF generation process...")

    const { inputs, results }: { inputs: TransformerInputs; results: TransformerResults } = await request.json()

    console.log("Received inputs:", JSON.stringify(inputs, null, 2))
    console.log("Received results:", JSON.stringify(results, null, 2))

    const scriptPath = path.join(process.cwd(), "scripts", "enhanced_pdf_filler.py")
    const inputPdfPath = path.join(process.cwd(), "public", "pdfvide.pdf")

    console.log("🔍 Checking file paths...")
    console.log("Script path:", scriptPath)
    console.log("Input PDF path:", inputPdfPath)

    if (!fs.existsSync(scriptPath)) {
      console.error("Python script not found:", scriptPath)
      throw new Error(`Python script not found: ${scriptPath}`)
    }
    if (!fs.existsSync(inputPdfPath)) {
      console.error("Input PDF not found:", inputPdfPath)
      throw new Error(`Input PDF not found: ${inputPdfPath}`)
    }

    console.log("All required files found")

    console.log("Generating PDF field mapping...")
    const mapper = new PDFFieldMapper()
    const pdfData = mapper.mapToPDFFields(inputs, results)

    console.log("Generated PDF field data:", JSON.stringify(pdfData, null, 2))

    const tempDataFile = path.join(process.cwd(), "temp_form_data.json")
    fs.writeFileSync(tempDataFile, JSON.stringify(pdfData, null, 2))

    console.log("Written temp data file:", tempDataFile)

    const timestamp = new Date().toISOString().replace(/[:.]/g, "-")
    const outputFilename = `transformer_project_${timestamp}.pdf`
    const outputPath = path.join(process.cwd(), outputFilename)

    console.log("Target output file:", outputPath)

    console.log("Executing Python script...")
    let command = `python3 "${scriptPath}" fill "${inputPdfPath}" "${tempDataFile}" "${outputPath}"`
    let result

    try {
      console.log("Running command:", command)
      result = await execAsync(command, { timeout: 30000 }) // 30 second timeout
    } catch (error) {
      console.log("python3 failed, trying python...")
      command = `python "${scriptPath}" fill "${inputPdfPath}" "${tempDataFile}" "${outputPath}"`
      console.log("Running command:", command)
      result = await execAsync(command, { timeout: 30000 })
    }

    const { stdout, stderr } = result

    console.log("Python stdout:", stdout)
    if (stderr) {
      console.error("Python stderr:", stderr)
    }

    // Clean up temp file
    console.log("Cleaning up temp data file...")
    if (fs.existsSync(tempDataFile)) {
      fs.unlinkSync(tempDataFile)
    }

    // Check if output file was created
    console.log("Checking if PDF was generated...")
    if (!fs.existsSync(outputPath)) {
      console.error("Generated PDF file not found:", outputPath)
      throw new Error(`Generated PDF file not found: ${outputPath}`)
    }

    console.log("PDF file generated successfully!")

    // Read the generated PDF file
    console.log("Reading generated PDF...")
    const pdfBuffer = fs.readFileSync(outputPath)
    console.log("PDF size:", pdfBuffer.length, "bytes")

    // Clean up the generated file
    console.log("Cleaning up generated PDF file...")
    fs.unlinkSync(outputPath)

    console.log("PDF generation completed successfully!")

    return new NextResponse(pdfBuffer, {
      headers: {
        "Content-Type": "application/pdf",
        "Content-Disposition": `attachment; filename="${outputFilename}"`,
        "Content-Length": pdfBuffer.length.toString(),
      },
    })
  } catch (error) {
    console.error("Error generating PDF:", error)

    // Clean up any temp files on error
    const tempDataFile = path.join(process.cwd(), "temp_form_data.json")
    if (fs.existsSync(tempDataFile)) {
      fs.unlinkSync(tempDataFile)
    }

    return NextResponse.json(
      {
        error: "Failed to generate PDF",
        details: error instanceof Error ? error.message : String(error),
      },
      { status: 500 },
    )
  }
}
