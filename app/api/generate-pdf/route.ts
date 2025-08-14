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
    console.log("Démarrage du processus de génération PDF...")

    const { inputs, results }: { inputs: TransformerInputs; results: TransformerResults } = await request.json()

    console.log("Entrées reçues:", JSON.stringify(inputs, null, 2))
    console.log("Résultats reçus:", JSON.stringify(results, null, 2))

    const scriptPath = path.join(process.cwd(), "scripts", "enhanced_pdf_filler.py")
    const inputPdfPath = path.join(process.cwd(), "public", "pdfvide.pdf")

    console.log("🔍 Vérification des chemins de fichiers...")
    console.log("Chemin du script:", scriptPath)
    console.log("Chemin du PDF d'entrée:", inputPdfPath)

    if (!fs.existsSync(scriptPath)) {
      console.error("Script Python non trouvé:", scriptPath)
      throw new Error(`Script Python non trouvé: ${scriptPath}`)
    }
    if (!fs.existsSync(inputPdfPath)) {
      console.error("PDF d'entrée non trouvé:", inputPdfPath)
      throw new Error(`PDF d'entrée non trouvé: ${inputPdfPath}`)
    }

    console.log("Tous les fichiers requis trouvés")

    console.log("Génération du mappage des champs PDF...")
    const mappeur = new PDFFieldMapper()
    const donneesPDF = mappeur.mapperVersChampsPDF(inputs, results)

    console.log("Données de champs PDF générées:", JSON.stringify(donneesPDF, null, 2))

    const fichierDonneesTemp = path.join(process.cwd(), "temp_form_data.json")
    fs.writeFileSync(fichierDonneesTemp, JSON.stringify(donneesPDF, null, 2))

    console.log("Fichier de données temporaire écrit:", fichierDonneesTemp)

    const horodatage = new Date().toISOString().replace(/[:.]/g, "-")
    const nomFichierSortie = `transformateur_projet_${horodatage}.pdf`
    const cheminSortie = path.join(process.cwd(), nomFichierSortie)

    console.log("Fichier de sortie cible:", cheminSortie)

    console.log("Exécution du script Python...")
    let commande = `python3 "${scriptPath}" fill "${inputPdfPath}" "${fichierDonneesTemp}" "${cheminSortie}"`
    let resultat

    try {
      console.log("Exécution de la commande:", commande)
      resultat = await execAsync(commande, { timeout: 30000 }) // Timeout de 30 secondes
    } catch (error) {
      console.log("python3 a échoué, essai avec python...")
      commande = `python "${scriptPath}" fill "${inputPdfPath}" "${fichierDonneesTemp}" "${cheminSortie}"`
      console.log("Exécution de la commande:", commande)
      resultat = await execAsync(commande, { timeout: 30000 })
    }

    const { stdout, stderr } = resultat

    console.log("Sortie Python stdout:", stdout)
    if (stderr) {
      console.error("Sortie Python stderr:", stderr)
    }

    // Nettoyer le fichier temporaire
    console.log("Nettoyage du fichier de données temporaire...")
    if (fs.existsSync(fichierDonneesTemp)) {
      fs.unlinkSync(fichierDonneesTemp)
    }

    // Vérifier si le fichier de sortie a été créé
    console.log("Vérification si le PDF a été généré...")
    if (!fs.existsSync(cheminSortie)) {
      console.error("Fichier PDF généré non trouvé:", cheminSortie)
      throw new Error(`Fichier PDF généré non trouvé: ${cheminSortie}`)
    }

    console.log("Fichier PDF généré avec succès!")

    // Lire le fichier PDF généré
    console.log("Lecture du PDF généré...")
    const tamponPDF = fs.readFileSync(cheminSortie)
    console.log("Taille du PDF:", tamponPDF.length, "octets")

    // Nettoyer le fichier généré
    console.log("Nettoyage du fichier PDF généré...")
    fs.unlinkSync(cheminSortie)

    console.log("Génération PDF terminée avec succès!")

    return new NextResponse(tamponPDF, {
      headers: {
        "Content-Type": "application/pdf",
        "Content-Disposition": `attachment; filename="${nomFichierSortie}"`,
        "Content-Length": tamponPDF.length.toString(),
      },
    })
  } catch (error) {
    console.error("Erreur lors de la génération du PDF:", error)

    // Nettoyer les fichiers temporaires en cas d'erreur
    const fichierDonneesTemp = path.join(process.cwd(), "temp_form_data.json")
    if (fs.existsSync(fichierDonneesTemp)) {
      fs.unlinkSync(fichierDonneesTemp)
    }

    return NextResponse.json(
      {
        error: "Échec de la génération du PDF",
        details: error instanceof Error ? error.message : String(error),
      },
      { status: 500 },
    )
  }
}
