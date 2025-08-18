import { NextResponse } from "next/server"
import { exec } from "child_process"
import { promisify } from "util"

const execAsync = promisify(exec)

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url)
    const limit = Number.parseInt(searchParams.get("limit") || "10")

    const { stdout, stderr } = await execAsync(`python scripts/get_history.py ${limit}`)

    if (stderr) {
      console.error("Erreur Python:", stderr)
      throw new Error(stderr)
    }

    const history = JSON.parse(stdout)

    return NextResponse.json({
      success: true,
      data: history,
    })
  } catch (error) {
    console.error("Erreur récupération historique:", error)
    return NextResponse.json({ error: "Erreur lors de la récupération de l'historique" }, { status: 500 })
  }
}

export async function DELETE(request: Request) {
  try {
    const { searchParams } = new URL(request.url)
    const id = Number.parseInt(searchParams.get("id") || "0")

    if (!id) {
      return NextResponse.json({ error: "ID manquant" }, { status: 400 })
    }

    const { stdout, stderr } = await execAsync(`python scripts/delete_calculation.py ${id}`)

    if (stderr) {
      console.error("Erreur Python:", stderr)
      throw new Error(stderr)
    }

    const result = JSON.parse(stdout)

    if (!result.success) {
      return NextResponse.json({ error: "Calcul non trouvé" }, { status: 404 })
    }

    return NextResponse.json({
      success: true,
      message: "Calcul supprimé avec succès",
    })
  } catch (error) {
    console.error("Erreur suppression:", error)
    return NextResponse.json({ error: "Erreur lors de la suppression" }, { status: 500 })
  }
}
