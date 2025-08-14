import { type NextRequest, NextResponse } from "next/server"
import { TransformerCalculator } from "@/lib/transformer-calculator"
import { PDFFieldMapper } from "@/lib/pdf-field-mapper"
import type { TransformerInputs } from "@/lib/types"

export async function POST(request: NextRequest) {
  try {
    const entrees: TransformerInputs = await request.json()

    if (!entrees.puissance_kva || !entrees.tension_primaire || !entrees.tension_secondaire) {
      return NextResponse.json(
        { error: "Paramètres requis manquants: puissance_kva, tension_primaire, tension_secondaire" },
        { status: 400 },
      )
    }

    const calculateur = new TransformerCalculator(entrees)

    const resultats = calculateur.calculerTout()

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
  } catch (error) {
    console.error("Erreur de calcul:", error)
    return NextResponse.json({ error: "Erreur interne de calcul" }, { status: 500 })
  }
}
