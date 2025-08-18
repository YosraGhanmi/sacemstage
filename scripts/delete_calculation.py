import sys
import json
from sqlalchemy.orm import sessionmaker
from setup_database import engine, TransformerCalculation

def delete_calculation(calc_id):
    """Supprimer un calcul par ID"""
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    try:
        calculation = session.query(TransformerCalculation)\
            .filter(TransformerCalculation.id == calc_id)\
            .first()
        
        if not calculation:
            return {"success": False, "message": "Calcul non trouvé"}
        
        session.delete(calculation)
        session.commit()
        
        return {"success": True, "message": "Calcul supprimé avec succès"}
        
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la suppression: {e}", file=sys.stderr)
        return {"success": False, "message": str(e)}
    finally:
        session.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(json.dumps({"success": False, "message": "ID manquant"}))
        sys.exit(1)
    
    calc_id = int(sys.argv[1])
    result = delete_calculation(calc_id)
    print(json.dumps(result))
