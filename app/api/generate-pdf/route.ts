import { type NextRequest, NextResponse } from "next/server"
import { exec } from "child_process"
import { promisify } from "util"
import fs from "fs"
import path from "path"

const execAsync = promisify(exec)

export async function POST(request: NextRequest) {
  try {
    const { formData, results } = await request.json()

    const scriptPath = path.join(process.cwd(), "scripts", "fill_pdf.py")
    const inputPdfPath = path.join(process.cwd(), "public", "pdfvide.pdf")

    if (!fs.existsSync(scriptPath)) {
      throw new Error(`Python script not found: ${scriptPath}`)
    }
    if (!fs.existsSync(inputPdfPath)) {
      throw new Error(`Input PDF not found: ${inputPdfPath}`)
    }

    const tempDataFile = path.join(process.cwd(), "temp_form_data.json")
    fs.writeFileSync(tempDataFile, JSON.stringify(formData))

    console.log("Executing Python script with paths:")
    console.log("Script:", scriptPath)
    console.log("Input PDF:", inputPdfPath)
    console.log("Temp data file:", tempDataFile)
    console.log("Form data:", formData)

    let command = `python3 "${scriptPath}" "${tempDataFile}" "${inputPdfPath}"`
    let result

    try {
      result = await execAsync(command)
    } catch (error) {
      console.log("python3 failed, trying python...")
      command = `python "${scriptPath}" "${tempDataFile}" "${inputPdfPath}"`
      result = await execAsync(command)
    }

    const { stdout, stderr } = result

    console.log("Python stdout:", stdout)
    if (stderr) {
      console.error("Python stderr:", stderr)
    }

    // Clean up temp file
    fs.unlinkSync(tempDataFile)

    // Extract output filename from Python script output
    const outputMatch = stdout.match(/SUCCESS:(.+)/)
    if (!outputMatch) {
      console.error("No SUCCESS output found in:", stdout)
      throw new Error("Failed to generate PDF - no success output")
    }

    const outputFilename = outputMatch[1].trim()
    const filePath = path.join(process.cwd(), outputFilename)

    // Check if file exists
    if (!fs.existsSync(filePath)) {
      throw new Error(`Generated PDF file not found: ${filePath}`)
    }

    // Read the generated PDF file
    const pdfBuffer = fs.readFileSync(filePath)

    // Clean up the temporary file
    fs.unlinkSync(filePath)

    return new NextResponse(pdfBuffer, {
      headers: {
        "Content-Type": "application/pdf",
        "Content-Disposition": `attachment; filename="${outputFilename}"`,
      },
    })
  } catch (error) {
    console.error("Error generating PDF:", error)
    return NextResponse.json({ error: "Failed to generate PDF", details: error }, { status: 500 })
  }
}
