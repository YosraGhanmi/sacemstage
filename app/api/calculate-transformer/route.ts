import { type NextRequest, NextResponse } from "next/server"
import { PDFFieldMapper } from "@/lib/pdf-field-mapper"
import type { TransformerInputs } from "@/lib/types"
import { exec } from "child_process"
import { promisify } from "util"

const execAsync = promisify(exec)

export async function POST(request: NextRequest) {
  try {
    const entrees: TransformerInputs = await request.json()

    if (!entrees.puissance_kva || !entrees.tension_primaire || !entrees.tension_secondaire) {
      return NextResponse.json(
        { error: "Paramètres requis manquants: puissance_kva, tension_primaire, tension_secondaire" },
        { status: 400 },
      )
    }

    const calculationType = entrees.calculation_type || "standard"
    const optimizationMode = entrees.optimization_mode || false

    const entreesJson = JSON.stringify({
      ...entrees,
      calculation_type: calculationType,
      optimization_mode: optimizationMode,
    })

    try {
      const { stdout, stderr } = await execAsync(`python scripts/transformer_calculator.py`, {
        env: {
          ...process.env,
          ENTREES_JSON: entreesJson,
        },
      })

      if (stderr) {
        console.error("Python calculation error:", stderr)
        throw new Error(`Python calculation failed: ${stderr}`)
      }

      const resultats = JSON.parse(stdout.trim())

      // Save calculation to database (existing functionality)
      try {
        const resultatsJson = JSON.stringify(resultats)

        const { stdout: saveStdout, stderr: saveStderr } = await execAsync(`python scripts/save_calculation.py`, {
          env: {
            ...process.env,
            ENTREES_JSON: entreesJson,
            RESULTATS_JSON: resultatsJson,
          },
        })

        if (saveStdout) {
          console.log(`Calcul sauvegardé: ${saveStdout.trim()}`)
        }
        if (saveStderr) {
          console.error("Avertissement base de données:", saveStderr)
        }
      } catch (dbError) {
        console.error("Erreur de sauvegarde en base:", dbError)
        // Continue même si la sauvegarde échoue
      }

      // Générer le mappage des champs PDF
      const mappeur = new PDFFieldMapper()
      const donneesPDF = mappeur.mapperVersChampsPDF(entrees, resultats)

      console.log("=== DONNÉES PDF GÉNÉRÉES ===")
      console.log(JSON.stringify(donneesPDF, null, 2))

      // Retourner les résultats avec le mappage PDF
      return NextResponse.json({
        ...resultats,
        mappageChampsPDF: donneesPDF,
      })
    } catch (pythonError) {
      console.error("Erreur d'exécution Python:", pythonError)
      throw pythonError
    }
  } catch (error) {
    console.error("Erreur de calcul:", error)
    return NextResponse.json({ error: "Erreur interne de calcul" }, { status: 500 })
  }
}
